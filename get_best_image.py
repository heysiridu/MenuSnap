import os
import json
import time
import requests
import webbrowser
from typing import List, Dict, Optional


# ============ configuration ============
GOOGLE_KEY = "AIzaSyBWjfsllZt7x3jwMaAu_P6VDUi9_e_URqM"
GOOGLE_CX  = "233a894886fd54a8a"


CANDIDATES_PER_DISH = 8
ALLOWED_MIME_PREFIX = ("image/",)


# ============ core functions ============


def search_google_images(query, count = 10):
   """
   search google images
   query: search query
   count: number of images to return
   return: list of images
   """
   if not (GOOGLE_KEY and GOOGLE_CX):
       print("missing GOOGLE_KEY or GOOGLE_CX")
       return []


   url = "https://www.googleapis.com/customsearch/v1"
   params = {
       "key": GOOGLE_KEY,
       "cx": GOOGLE_CX,
       "q": query,
       "searchType": "image",
       "num": min(10, count),
       "safe": "high",
   }
   r = requests.get(url, params=params, timeout=15)
   try:
       r.raise_for_status()
   except Exception as e:
       print("request failed: ", e, "\nresponse content: ", r.text)
       return []
   data = r.json()
   return data.get("items", [])




def pick_best_image_from_google(items, top_n=3):
   """
   pick the best image from google images
   items: list of images
   top_n: number of images to return
   return: list of images
   """
   candidates = []
  
   for x in items:
       link = x.get("link")
       image = x.get("image", {}) or {}
       width = image.get("width")
       height = image.get("height")
       mime = image.get("mime")
      
       if not link or not width or not height:
           continue
       if mime and not mime.startswith(ALLOWED_MIME_PREFIX):
           continue
      
       area = (width or 0) * (height or 0)
       candidates.append({
           "url": link,
           "width": width,
           "height": height,
           "area": area,
           "title": x.get("title"),
           "contextLink": image.get("contextLink") or x.get("link"),
       })
  
   candidates.sort(key=lambda img: img["area"], reverse=True)
  
   result = candidates[:top_n]
   for img in result:
       img.pop("area", None)
  
   return result




def best_image_for_dish(dish_name):
   """
   get the best image for a dish
   dish_name: dish name
   return: list of images
   """
   query = f"{dish_name} food"
   items_g = search_google_images(query, count=CANDIDATES_PER_DISH)
   best_images = pick_best_image_from_google(items_g, top_n=5)
   return best_images


def verify_image_url(url, timeout=5):
   try:
       problematic_domains = ['instagram.com', 'facebook.com', 'twitter.com']
       if any(domain in url.lower() for domain in problematic_domains):
           return False
       
       headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
       }
       response = requests.head(url, timeout=timeout, allow_redirects=True, headers=headers)
       
       if response.status_code != 200:
           return False
       
       content_type = response.headers.get('Content-Type', '').lower()
       if content_type and not content_type.startswith('image/'):
           return False
       
       return True
   except:
       return False


def get_valid_image_for_dish(dish_name, verbose=True):
   """
   get the valid image for a dish
   dish_name: dish name
   verbose: whether to print verbose output
   return: valid image
   """
   candidate_images = best_image_for_dish(dish_name)
  
   if not candidate_images:
       if verbose:
           print("no candidate images found")
       return None
  
   for i, img in enumerate(candidate_images, 1):
       if verbose:
           print(f"try candidate {i}/{len(candidate_images)}: {img['width']}x{img['height']}")
      
       if verify_image_url(img["url"]):
           if verbose:
               print(f"find accessible image")
           return img
       else:
           if verbose:
               print(f"image is not accessible")
  
   if verbose:
       print("all candidate images are not accessible")
   return None
def main():
   sample_input = [
       {"dish": "Drunken Raw Crab"},
       {"dish": "Surströmming"}
   ]


   for item in sample_input:
       dish = item["dish"]
       print(f"\nsearching: {dish}")
      
       img = get_valid_image_for_dish(dish, verbose=True)
      
       if img:
           print(json.dumps(img, ensure_ascii=False, indent=2))
           webbrowser.open(img["url"])
       else:
           print("no valid image found")
      
       time.sleep(0.2)




if __name__ == "__main__":
   main()
