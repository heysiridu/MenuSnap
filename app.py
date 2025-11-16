from flask import Flask, request, jsonify
import os
# import time # 不再需要
# from werkzeug.utils import secure_filename # 不再需要

print("[app.py] 正在导入 ocr.paddle_service...")
from ocr import paddle_service
print("[app.py] 导入完成。")


app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))

# 配置图片源目录
IMAGE_SOURCE_FOLDER = os.path.join(script_dir, './images')

# 检查源目录是否存在
if not os.path.isdir(IMAGE_SOURCE_FOLDER):
    print(f"[app.py] 警告：配置的源目录不存在: {IMAGE_SOURCE_FOLDER}")
    print("[app.py] 请创建该目录，或在 app.py 中修改 IMAGE_SOURCE_FOLDER 变量")
else:
    print(f"[app.py] 将从以下目录读取图片: {IMAGE_SOURCE_FOLDER}")

app.config['IMAGE_SOURCE_FOLDER'] = IMAGE_SOURCE_FOLDER




@app.route('/predict', methods=['POST'])
def predict():
    """
    接收包含 'filename' 的 JSON 请求，
    从指定的文件夹中读取该文件，使用 OCR 服务进行推理，并返回 JSON 结果。
    """

    if not request.is_json:
        return jsonify({"error": "请求必须是 application/json 格式"}), 400

    data = request.get_json()

    if 'filename' not in data:
        return jsonify({"error": "JSON 请求中未找到 'filename' 键"}), 400

    filename = data['filename']


    if not filename:
        return jsonify({"error": "filename 不能为空"}), 400


    base_dir = app.config['IMAGE_SOURCE_FOLDER']
    target_path = os.path.join(base_dir, filename)


    base_dir_real = os.path.realpath(base_dir)
    target_path_real = os.path.realpath(target_path)

    if not target_path_real.startswith(base_dir_real):
        print(f"[app.py] 安全警告：检测到路径遍历尝试。拒绝访问: {filename}")
        return jsonify({"error": "非法的文件路径"}), 403 # 403 Forbidden

    # 6. 检查文件是否存在
    if not os.path.exists(target_path_real):
        return jsonify({"error": f"文件 '{filename}' 在指定目录中不存在"}), 404 # 404 Not Found

    try:
        result = paddle_service.predict_text_only(target_path_real)
        
    except Exception as e:
        return jsonify({"error": f"处理文件时出错: {str(e)}"}), 500
    finally:
        pass

    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify(result), 500

if __name__ == '__main__':
    # 启动服务器
    print("[app.py] 启动 Flask 服务器...")
    app.run(host='0.0.0.0', port=5001, debug=False)