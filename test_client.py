import requests
import json

# API 服务器的地址
url = 'http://127.0.0.1:5001/predict'

filename_on_server = 'menu6.png'

# 准备要发送的 JSON 数据
payload = {
    'filename': filename_on_server
}

try:
    print(f"向 {url} 发送 POST 请求 (JSON)...")
    # --- 修改 ---
    # 使用 'json=' 参数来自动设置 Content-Type: application/json
    response = requests.post(url, json=payload)
    
    # 打印格式化的 JSON 响应
    print("\n--- API 响应 (JSON) ---")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))

except requests.exceptions.ConnectionError:
    print(f"错误：无法连接到 {url}。请确保 app.py 服务器正在运行。")
except Exception as e:
    print(f"发生了一个错误: {e}")