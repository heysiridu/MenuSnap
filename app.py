from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

from get_best_image import get_valid_image_for_dish

print("[app.py] Loading OCR service...")
from ocr import paddle_service
print("[app.py] OCR service loaded.")

app = Flask(__name__)

def is_valid_dish_name(text):
    if not text or len(text.strip()) < 3:
        return False
    
    text = text.strip()
    
    if re.match(r'^[\d\s\-\.]+$', text):
        return False
    
    if re.match(r'^\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$', text):
        return False
    
    address_keywords = ['st.', 'street', 'ave', 'avenue', 'rd', 'road', 
                       'blvd', 'boulevard', 'dr', 'drive', 'city', 'zip']
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in address_keywords):
        return False
    
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > len(text) * 0.5:
        return False
    
    ignore_list = [
        'menu', 'hours', 'open', 'closed', 'phone', 'address',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 
        'saturday', 'sunday', 'website', 'email', 'contact'
    ]
    if text_lower in ignore_list:
        return False
    
    if not re.search(r'[a-zA-Z]{2,}', text):
        return False
    
    return True

def filter_dish_names(menu_items):
    filtered = []
    for item in menu_items:
        dish_name = item.get('dish', '')
        if is_valid_dish_name(dish_name):
            filtered.append(item)
        else:
            print(f"[Filter] Filtered out non-dish: {dish_name}")
    
    return filtered

script_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_SOURCE_FOLDER = os.path.join(script_dir, './images')
app.config['IMAGE_SOURCE_FOLDER'] = IMAGE_SOURCE_FOLDER

CORS(app, resources={
   r"/api/*": {
       "origins": ["http://localhost:3000"], 
       "methods": ["GET", "POST", "OPTIONS"],
       "allow_headers": ["Content-Type"]
   }
})

@app.route('/api/health', methods=['GET'])
def health_check():
   return jsonify({
       'status': 'ok',
       'service': 'dish-image-api'
   })

@app.route('/api/dish-image', methods=['POST'])
def get_dish_image():
   try:
       data = request.get_json()
      
       if not data:
           return jsonify({
               'success': False,
               'error': 'No JSON data provided'
           }), 400
      
       dish_name = data.get('dish')
      
       if not dish_name:
           return jsonify({
               'success': False,
               'error': 'Missing required field: dish'
           }), 400
      
       image = get_valid_image_for_dish(dish_name, verbose=False)
      
       if image:
           return jsonify({
               'success': True,
               'data': image
           }), 200
       else:
           return jsonify({
               'success': False,
               'error': 'No valid image found for this dish'
           }), 404
          
   except Exception as e:
       print(f"Error in get_dish_image: {str(e)}")
       return jsonify({
           'success': False,
           'error': f'Internal server error: {str(e)}'
       }), 500

@app.route('/api/ocr/predict', methods=['POST'])
def ocr_predict():
   try:
       if not request.is_json:
           return jsonify({"error": "Request must be application/json"}), 400

       data = request.get_json()

       if 'filename' not in data:
           return jsonify({"error": "Missing 'filename' key in request"}), 400

       filename = data['filename']

       if not filename:
           return jsonify({"error": "Filename cannot be empty"}), 400

       base_dir = app.config['IMAGE_SOURCE_FOLDER']
       target_path = os.path.join(base_dir, filename)

       base_dir_real = os.path.realpath(base_dir)
       target_path_real = os.path.realpath(target_path)

       if not target_path_real.startswith(base_dir_real):
           return jsonify({"error": "Invalid file path"}), 403

       if not os.path.exists(target_path_real):
           return jsonify({"error": f"File '{filename}' not found in directory"}), 404

       result = paddle_service.predict_text_only(target_path_real)
       
       if result.get('success'):
           menu_items = result.get('menu_items', [])
           filtered_items = filter_dish_names(menu_items)
           
           result['menu_items'] = filtered_items
           result['original_count'] = len(menu_items)
           result['filtered_count'] = len(filtered_items)
           
           return jsonify(result)
       else:
           return jsonify(result), 500
           
   except Exception as e:
       print(f"Error in ocr_predict: {str(e)}")
       return jsonify({
           'success': False,
           'error': f'Internal server error: {str(e)}'
       }), 500

@app.route('/api/menu/ocr-with-images', methods=['POST'])
def ocr_with_images():
   try:
       if not request.is_json:
           return jsonify({"error": "Request must be application/json"}), 400

       data = request.get_json()
       filename = data.get('filename')

       if not filename:
           return jsonify({
               'success': False,
               'error': 'Missing required field: filename'
           }), 400

       base_dir = app.config['IMAGE_SOURCE_FOLDER']
       target_path = os.path.join(base_dir, filename)
       
       if not os.path.exists(target_path):
           return jsonify({
               'success': False,
               'error': f'File not found: {filename}'
           }), 404

       ocr_result = paddle_service.predict_text_only(target_path)
       
       if not ocr_result.get('success'):
           return jsonify({
               'success': False,
               'error': 'OCR recognition failed'
           }), 500

       menu_items = ocr_result.get('menu_items', [])
       
       print(f"[OCR+Image] OCR detected {len(menu_items)} items")
       filtered_items = filter_dish_names(menu_items)
       print(f"[OCR+Image] After filtering: {len(filtered_items)} valid dishes")
       
       results = []
       for item in filtered_items:
           dish_name = item.get('dish', '')
           if dish_name:
               print(f"[OCR+Image] Searching image for '{dish_name}'...")
               image = get_valid_image_for_dish(dish_name, verbose=False)
               results.append({
                   'dish': dish_name,
                   'image': image
               })

       return jsonify({
           'success': True,
           'ocr_time': ocr_result.get('inference_time_seconds', 0),
           'dishes_found': len(results),
           'menu_with_images': results
       })

   except Exception as e:
       print(f"Error in ocr_with_images: {str(e)}")
       return jsonify({
           'success': False,
           'error': f'Internal server error: {str(e)}'
       }), 500

@app.errorhandler(404)
def not_found(error):
   return jsonify({
       'success': False,
       'error': 'Endpoint not found'
   }), 404

@app.errorhandler(500)
def internal_error(error):
   return jsonify({
       'success': False,
       'error': 'Internal server error'
   }), 500

if __name__ == '__main__':
   app.run(
       host='0.0.0.0', 
       port=5001,
       debug=True 
   )
