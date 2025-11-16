# PaddleOCR 文字识别 API 服务

本项目是一个基于 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [Flask](https://flask.palletsprojects.com/) 搭建的轻量级光学字符识别 (OCR) API 服务。

它被设计为在服务器上运行，并从一个**指定的本地文件夹**中读取图片进行文字识别，而不是通过 HTTP 上传。这使其非常适用于受控的服务器环境或批处理任务。

## 🚀 主要特性

* **高精度识别:** 利用 PaddleOCR 的强大功能，支持中英文、数字等多种文字的高精度识别。
* **API 服务化:** 通过 Flask 封装，提供简单易用的 `POST /predict` JSON 接口，易于被其他服务（如 Python, Java, curl）调用。
* **模型单例模式:** OCR 服务在启动时以单例模式加载。这确保模型和依赖（如 `ocr/paddle_service.py` 所示）只在内存中初始化一次，极大地提高了后续 API 请求的响应速度。
* **安全可控:** 从服务器本地文件夹读取文件，避免了处理文件上传的安全风险和复杂性，同时通过安全检查防止了路径遍历攻击。

