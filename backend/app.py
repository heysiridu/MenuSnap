from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import re
import uuid
from deep_translator import GoogleTranslator

# 导入业务逻辑
from get_best_image import get_valid_image_for_dish

print("[app.py] Loading OCR service...")
from ocr import paddle_service
print("[app.py] OCR service loaded.")

app = Flask(__name__)


# --- 辅助函数：校验是否为有效菜名 ---
def is_valid_dish_name(text):
    if not text or len(text.strip()) < 3:
        return False
    
    text = text.strip()
    
    # 排除纯数字或符号
    if re.match(r'^[\d\s\-\.]+$', text):
        return False
    
    # 排除电话号码格式
    if re.match(r'^\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$', text):
        return False
    
    # 排除地址关键词
    address_keywords = ['st.', 'street', 'ave', 'avenue', 'rd', 'road', 
                       'blvd', 'boulevard', 'dr', 'drive', 'city', 'zip']
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in address_keywords):
        return False
    
    # 排除数字占比过高的文本
    digit_count = sum(c.isdigit() for c in text)
    if digit_count > len(text) * 0.5:
        return False
    
    # 排除通用无意义词汇
    ignore_list = [
        'menu', 'hours', 'open', 'closed', 'phone', 'address',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 
        'saturday', 'sunday', 'website', 'email', 'contact'
    ]
    if text_lower in ignore_list:
        return False
    
    # 必须包含字母
    if not re.search(r'[a-zA-Z]{2,}', text):
        return False
    
    return True

# --- 辅助函数：过滤列表 ---
def filter_dish_names(menu_items):
    filtered = []
    for item in menu_items:
        dish_name = item.get('dish', '')
        if is_valid_dish_name(dish_name):
            filtered.append(item)
        else:
            print(f"[Filter] Filtered out non-dish: {dish_name}")
    return filtered

# --- 核心函数：批量翻译菜名 ---
def get_batch_translations(dish_names):
    if not dish_names:
        return {}
    
    translations_map = {}
    try:
        print(f"[Translate] Processing {len(dish_names)} items...")
        
        # 创建翻译实例
        translator_zh = GoogleTranslator(source='auto', target='zh-CN')
        translator_es = GoogleTranslator(source='auto', target='es')

        for name in dish_names:
            # deep-translator 翻译单个词非常快
            zh_text = translator_zh.translate(name)
            es_text = translator_es.translate(name)
            
            translations_map[name] = {
                "en": name,
                "zh": zh_text,
                "es": es_text
            }
        return translations_map
    except Exception as e:
        print(f"[Translate Error] {e}")
        return {name: {"en": name, "zh": name, "es": name} for name in dish_names}

# --- 配置 ---
script_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_SOURCE_FOLDER = os.path.join(script_dir, './images')
app.config['IMAGE_SOURCE_FOLDER'] = IMAGE_SOURCE_FOLDER

CORS(app, resources={
   r"/api/*": {
       "origins": ["*"],
       "methods": ["GET", "POST", "OPTIONS"],
       "allow_headers": ["Content-Type"]
   }
})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 路由：上传并处理图片 ---
@app.route('/api/upload-and-process', methods=['POST'])
def upload_and_process():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # 保存文件
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['IMAGE_SOURCE_FOLDER'], unique_filename)
        os.makedirs(app.config['IMAGE_SOURCE_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        print(f"[Upload] File saved, starting OCR...")
        
        # OCR 识别
        ocr_result = paddle_service.predict_text_only(filepath)
        if not ocr_result.get('success'):
            return jsonify({'success': False, 'error': 'OCR recognition failed'}), 500
        
        menu_items = ocr_result.get('menu_items', [])
        filtered_items = filter_dish_names(menu_items)
        
        # 准备翻译
        raw_names = [item.get('dish', '') for item in filtered_items]
        translations_map = get_batch_translations(raw_names)
        
        # 组装结果
        results = []
        for item in filtered_items:
            dish_name = item.get('dish', '')
            if dish_name:
                print(f"[Upload] Searching image for '{dish_name}'...")
                image = get_valid_image_for_dish(dish_name, verbose=False)
                results.append({
                    'dish': dish_name,
                    'translations': translations_map.get(dish_name), # 动态翻译结果
                    'price': item.get('price', ''),
                    'image': image
                })
        
        return jsonify({
            'success': True,
            'ocr_time': ocr_result.get('inference_time_seconds', 0),
            'dishes_found': len(results),
            'menu_with_images': results
        })
        
    except Exception as e:
        print(f"Error in upload_and_process: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# --- 路由：OCR + 搜图 (Demo 模式) ---
@app.route('/api/menu/ocr-with-images', methods=['POST'])
def ocr_with_images():
   try:
       data = request.get_json()
       filename = data.get('filename')
       if not filename:
           return jsonify({'success': False, 'error': 'Missing filename'}), 400

       base_dir = app.config['IMAGE_SOURCE_FOLDER']
       target_path = os.path.join(base_dir, filename)
       if not os.path.exists(target_path):
           return jsonify({'success': False, 'error': 'File not found'}), 404

       ocr_result = paddle_service.predict_text_only(target_path)
       if not ocr_result.get('success'):
           return jsonify({'success': False, 'error': 'OCR failed'}), 500

       filtered_items = filter_dish_names(ocr_result.get('menu_items', []))
       
       # 批量翻译
       raw_names = [item.get('dish', '') for item in filtered_items]
       translations_map = get_batch_translations(raw_names)
       
       results = []
       for item in filtered_items:
           dish_name = item.get('dish', '')
           if dish_name:
               image = get_valid_image_for_dish(dish_name, verbose=False)
               results.append({
                   'dish': dish_name,
                   'translations': translations_map.get(dish_name),
                   'image': image
               })

       return jsonify({
           'success': True,
           'ocr_time': ocr_result.get('inference_time_seconds', 0),
           'dishes_found': len(results),
           'menu_with_images': results
       })

   except Exception as e:
       return jsonify({'success': False, 'error': str(e)}), 500

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
   return jsonify({'status': 'ok', 'service': 'dish-image-api'})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)