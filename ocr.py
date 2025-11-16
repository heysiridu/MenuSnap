from paddleocr import PaddleOCR
import time
import os
from typing import List, Dict, Any

class PaddleOCRService:
    """
    PaddleOCR 服务类：
    1. 使用 __new__ 方法实现严格的单例模式 (Singleton)。
    2. 对外提供统一的预测接口 (predict_text_only)。
    3. 在初始化时加载 PaddleOCR 模型 (Maas 启动阶段)。
    """
    
    # 类变量，用于存储唯一的实例
    _instance = None
    # 存储 OCR 引擎对象
    ocr_engine = None

    def __new__(cls, *args, **kwargs):
        """
        重写 __new__ 方法，确保只创建一个实例。
        """
        if cls._instance is None:
            # 第一次创建实例时，初始化模型
            print("🚀 [Maas Service] 正在初始化 PaddleOCR 服务 (单例实现)...")
            cls._instance = super(PaddleOCRService, cls).__new__(cls)
            cls._instance.initialize_model()
            print(f"✅ [Maas Service] PaddleOCR 服务初始化完成。ID: {id(cls._instance)}")
        else:
            print(">>> [Maas Service] 实例已存在，直接返回唯一实例。")
        return cls._instance

    def initialize_model(self):
        """
        进行模型初始化操作，只在单例首次创建时调用。
        """
        start_init = time.time()
        try:
            # 这里的 self 指向 _instance
            self.ocr_engine = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                # 推荐添加 use_gpu=False/True 根据部署环境设置
                # use_gpu=True 
            )
        except Exception as e:
            print(f"❌ [Maas Service] 模型初始化失败: {e}")
            raise e
            
        end_init = time.time()
        print(f"⏱️ 模型初始化/加载耗时: {end_init - start_init:.4f} 秒")

    def predict_text_only(self, input_path: str) -> Dict[str, Any]:
        """
        对外暴露的预测接口，执行 OCR 推理并只返回识别出的文本。
        
        Args:
            input_path: 输入图片的本地路径。
            
        Returns:
            包含推理结果和耗时的字典。
        """
        if not os.path.exists(input_path):
            return {"error": f"未找到输入文件: {input_path}", "success": False}
        
        if self.ocr_engine is None:
            return {"error": "OCR 引擎未初始化。", "success": False}

        print(f"\n[Maas Call] 开始对图像 '{input_path}' 执行推理...")
        
        start_predict = time.time()
        try:
            # 执行 OCR 推理
            result = self.ocr_engine.predict(input=input_path)
        except Exception as e:
            return {"error": f"推理过程中发生错误: {e}", "success": False}
        end_predict = time.time()
        
        predict_duration = end_predict - start_predict
        all_rec_texts=[]
        for rec in result:
            all_rec_texts=rec["rec_texts"]

        
        print(f"⏱️ 推理耗时: {predict_duration:.4f} 秒")
        
        return {
            "success": True,
            "inference_time_seconds": predict_duration,
            "rec_texts": all_rec_texts
        }


paddle_service=PaddleOCRService()

