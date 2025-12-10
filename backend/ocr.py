from paddleocr import PaddleOCR
import time
import os
import numpy as np
from typing import List, Dict, Any
import re

class PaddleOCRService:
    _instance = None
    ocr_engine = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("[OCR Service] Initializing PaddleOCR service...")
            cls._instance = super(PaddleOCRService, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance

    def initialize_model(self):
        try:
            self.ocr_engine = PaddleOCR(
                use_angle_cls=False,
                lang="ch",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                ocr_version='PP-OCRv4' 
            )
        except Exception as e:
            print(f"Model initialization failed: {e}")
            raise e

    def predict_text_only(self, input_path: str) -> Dict[str, Any]:
        if not os.path.exists(input_path):
            return {"error": f"File not found: {input_path}", "success": False}

        start_predict = time.time()
        try:
            result = self.ocr_engine.predict(input_path)
        except Exception as e:
            return {"error": f"Inference error: {e}", "success": False}
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
                        "cy": y_center,
                        "cx": x_left,
                        "y_min": y_min,
                        "y_max": y_max
                    })
        
        structured_menu = self._post_process_menu(raw_items)
        predict_duration = end_predict - start_predict
        
        print(f"[DEBUG] Raw OCR text count: {len(raw_items)}")
        if raw_items:
            print("[DEBUG] First 5 raw texts:")
            for item in raw_items[:5]:
                print(f"  - {item['text']}")
        else:
            print("[DEBUG] WARNING: OCR detected no text!")
        print(f"[DEBUG] Processed menu item count: {len(structured_menu)}")
        
        return {
            "success": True,
            "inference_time_seconds": predict_duration,
            "menu_items": structured_menu
        }

    def _post_process_menu(self, items: List[Dict]) -> List[Dict]:
        if not items:
            return []

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

        price_anchors = []
        text_candidates = []
        
        def is_price_token(s):
            clean = s.replace('$', '').replace('starting at', '').strip()
            if not clean:
                return False
            
            if any(char.isdigit() for char in clean) and len(clean) < 8:
                return True
            
            if re.search(r'-\d+\.?\d*$', s):
                return True
            
            return False

        for line_items in lines:
            text_parts = []
            has_price_in_line = False
            
            avg_y = sum([i['cy'] for i in line_items]) / len(line_items)

            for item in line_items:
                txt = item['text']
                if is_price_token(txt):
                    has_price_in_line = True
                    if '-' in txt and re.search(r'-\d+\.?\d*$', txt):
                        dish_name = re.sub(r'-\d+\.?\d*$', '', txt).strip()
                        if dish_name:
                            text_parts.append(dish_name)
                else:
                    text_parts.append(txt)
            
            clean_text = " ".join(text_parts).strip()
            clean_text = re.sub(r'^[\d\.]+\s+', '', clean_text)
            
            line_obj = {
                "text": clean_text,
                "y": avg_y,
                "has_price": has_price_in_line
            }

            if clean_text:
                text_candidates.append(line_obj)
            
            if has_price_in_line:
                price_anchors.append(line_obj)

        found_dishes = set()
        
        IGNORE_EXACT = ["SALAD", "SIDES", "DRINKS", "NEW!", "RICE BOWL", "EXTRAS"]

        for p_anchor in price_anchors:
            best_match_text = None
            
            if p_anchor['text']:
                best_match_text = p_anchor['text']
            
            elif text_candidates:
                closest_candidate = min(text_candidates, key=lambda c: abs(c['y'] - p_anchor['y']))
                
                if abs(closest_candidate['y'] - p_anchor['y']) < 120:
                    best_match_text = closest_candidate['text']

            if best_match_text:
                if best_match_text not in IGNORE_EXACT and len(best_match_text) > 2:
                    found_dishes.add(best_match_text)

        result_list = [{"dish": name} for name in found_dishes]
        
        return result_list
    

paddle_service = PaddleOCRService()
