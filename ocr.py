from paddleocr import PaddleOCR
import time
import os
import numpy as np
from typing import List, Dict, Any
import numpy as np
class PaddleOCRService:
    _instance = None
    ocr_engine = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("🚀 [Maas Service] 正在初始化 PaddleOCR 服务...")
            cls._instance = super(PaddleOCRService, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance

    def initialize_model(self):
        try:
            self.ocr_engine = PaddleOCR(
                # 核心设置：关闭角度分类，指定语言
                use_angle_cls=False,
                lang="ch",
                
                # --- 关键设置 ---
                # 1. 禁用文档方向分类 (解决 No valid model found 报错)
                use_doc_orientation_classify=False,
                
                # 2. 禁用文档矫正 (加快速度，减少模型依赖)
                use_doc_unwarping=False,
                
                # 注意：已删除 use_textline_orientation 参数以解决互斥报错
                
                # 指定模型版本，确保稳定性
                ocr_version='PP-OCRv4' 
            )
        except Exception as e:
            print(f"❌ 模型初始化失败: {e}")
            raise e
    # 修改 ocr.py 中的 predict_text_only 方法
    def predict_text_only(self, input_path: str) -> Dict[str, Any]:
        if not os.path.exists(input_path):
            return {"error": f"未找到文件: {input_path}", "success": False}

        start_predict = time.time()
        try:
            result = self.ocr_engine.predict(input_path)
        except Exception as e:
            return {"error": f"推理错误: {e}", "success": False}
        end_predict = time.time()
        
        raw_items = []
        
        if result:
            res_list = list(result)
            if len(res_list) > 0:
                data = res_list[0]
                texts = data.get('rec_texts', [])
                boxes = data.get('dt_polys', [])
                
                for text, box in zip(texts, boxes):
                    box_np = np.array(box) 
                    
                    y_min = np.min(box_np[:, 1])
                    y_max = np.max(box_np[:, 1])
                    y_center = (y_min + y_max) / 2
                    x_left = np.min(box_np[:, 0])

                    raw_items.append({
                        "text": text,
                        "cy": y_center,  # 中心点
                        "cx": x_left,    # 左侧点
                        "y_min": y_min,  # [新增] 顶部边界
                        "y_max": y_max   # [新增] 底部边界
                    })
        
        structured_menu = self._post_process_menu(raw_items)
        predict_duration = end_predict - start_predict
        
        return {
            "success": True,
            "inference_time_seconds": predict_duration,
            "menu_items": structured_menu
        }
    # 修改 ocr.py 中的 _post_process_menu 方法
    def _post_process_menu(self, items: List[Dict]) -> List[Dict]:
        """
        全局空间锚点搜索 (Global Spatial Anchor Search):
        
        核心思想：
        不再按行顺序读取，而是将 OCR 结果视为二维点阵。
        1. 找出所有“价格锚点”。
        2. 找出所有“文本候选块”。
        3. 对于每个价格，在全局范围内寻找“垂直距离最近”的文本块作为其菜名。
        """
        if not items:
            return []

        # --- 1. 预处理：几何行合并 (Geometry Line Merge) ---
        # 目的：将碎片化的单词 (如 "Kung", "Pao", "Chicken") 合并成一个完整的文本块。
        # 这步必须保留，否则“距离最近”的可能只是 "Chicken" 这个词，而不是整道菜名。
        items.sort(key=lambda k: k['cy'])
        lines = []
        for item in items:
            added = False
            if lines:
                last_line = lines[-1]
                l_min = sum([i['y_min'] for i in last_line]) / len(last_line)
                l_max = sum([i['y_max'] for i in last_line]) / len(last_line)
                
                intersection = max(0, min(l_max, item['y_max']) - max(l_min, item['y_min']))
                union = (item['y_max'] - item['y_min'])
                if union > 0 and (intersection / union) > 0.4:
                    last_line.append(item)
                    added = True
            if not added:
                lines.append([item])

        # --- 2. 构建“价格集合”与“文本集合” ---
        price_anchors = []    # 存放价格信息的块
        text_candidates = []  # 存放潜在菜名的块
        
        import re
        
        def is_price_token(s):
            clean = s.replace('$', '').replace('starting at', '').strip()
            if not clean: return False
            return (any(char.isdigit() for char in clean) and len(clean) < 8)

        for line_items in lines:
            # 提取该行的属性
            text_parts = []
            has_price_in_line = False
            
            # 计算该行的几何中心 Y
            avg_y = sum([i['cy'] for i in line_items]) / len(line_items)

            for item in line_items:
                txt = item['text']
                if is_price_token(txt):
                    has_price_in_line = True
                else:
                    text_parts.append(txt)
            
            clean_text = " ".join(text_parts).strip()
            # 清理行首编号
            clean_text = re.sub(r'^[\d\.]+\s+', '', clean_text)
            
            # 构造行对象
            line_obj = {
                "text": clean_text,
                "y": avg_y,
                "has_price": has_price_in_line
            }

            # 分类归档
            # A. 如果这一行有文本，它就是潜在的菜名候选者
            if clean_text:
                text_candidates.append(line_obj)
            
            # B. 如果这一行有价格，它就是一个搜索锚点
            if has_price_in_line:
                price_anchors.append(line_obj)

        # --- 3. 核心逻辑：最近邻搜索 (Nearest Neighbor) ---
        found_dishes = set() # 使用集合自动去重
        
        # 黑名单
        IGNORE_EXACT = ["SALAD", "SIDES", "DRINKS", "NEW!", "RICE BOWL", "EXTRAS"]

        for p_anchor in price_anchors:
            best_match_text = None
            
            # 情况 1: 同行匹配 (Horizontal Match)
            # 价格锚点本身就包含文本 -> 距离为 0 -> 直接锁定
            if p_anchor['text']:
                best_match_text = p_anchor['text']
            
            # 情况 2: 异行匹配 (Vertical Match)
            # 价格锚点只有价格 (如 "$12.99") -> 在所有文本候选者中找最近的
            elif text_candidates:
                # 使用 min 函数寻找垂直距离 abs(y1 - y2) 最小的行
                closest_candidate = min(text_candidates, key=lambda c: abs(c['y'] - p_anchor['y']))
                
                # 安全阈值检查：防止匹配到页脚或太远的地方 (比如 > 100px)
                if abs(closest_candidate['y'] - p_anchor['y']) < 120:
                    best_match_text = closest_candidate['text']

            # --- 保存结果 ---
            if best_match_text:
                # 过滤垃圾词
                if best_match_text not in IGNORE_EXACT and len(best_match_text) > 2:
                    found_dishes.add(best_match_text)

        # --- 4. 格式化输出 ---
        # 将 set 转回 list dict
        result_list = [{"dish": name} for name in found_dishes]
        
        return result_list
    

paddle_service = PaddleOCRService()