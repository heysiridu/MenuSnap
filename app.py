from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

from get_best_image import get_valid_image_for_dish, search_google_images, pick_best_image_from_google

app = Flask(__name__)

# clear react server access
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],  
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ============ API Routes ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    health check endpoint
    """
    return jsonify({
        'status': 'ok',
        'service': 'dish-image-api'
    })


@app.route('/api/dish-image', methods=['POST'])
def get_dish_image():
    """
    get the image for a dish
    """
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


# ============ Error Handlers ============

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


# ============ Main ============

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  
        port=5001,
        debug=True  
    )