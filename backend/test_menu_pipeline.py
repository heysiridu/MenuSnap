import requests
import json

BASE_URL = "http://localhost:5001"

def test_ocr_with_images():
    print("\n" + "="*60)
    print("TEST: OCR + Image Search Complete Pipeline")
    print("="*60)
    
    url = f"{BASE_URL}/api/menu/ocr-with-images"
    payload = {"filename": "menu2.png"}
    
    print(f"\nSending request to: {url}")
    print(f"Request data: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        
        print(f"\nResponse status code: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"\nSuccessfully recognized menu!")
            print(f"   OCR time: {result.get('ocr_time', 0):.2f} seconds")
            print(f"   Dishes found: {result.get('dishes_found', 0)}")
            
            menu = result.get('menu_with_images', [])
            print(f"\nMenu details ({len(menu)} dishes):")
            
            for i, item in enumerate(menu, 1):
                dish = item.get('dish', 'Unknown')
                image = item.get('image')
                
                print(f"\n   {i}. {dish}")
                if image:
                    url = image.get('url', 'N/A')
                    print(f"      Image URL:")
                    print(f"         {url}")
                    print(f"      Size: {image.get('width')}x{image.get('height')}")
                    print(f"      Title: {image.get('title', 'N/A')}")
                else:
                    print(f"      No image found")
        else:
            print(f"\nFailed: {result.get('error', 'Unknown error')}")
    
    except requests.exceptions.ConnectionError:
        print(f"\nError: Cannot connect to {BASE_URL}")
        print("   Please make sure server is running: python app.py")
    except Exception as e:
        print(f"\nError: {str(e)}")


def test_ocr_only():
    print("\n" + "="*60)
    print("TEST: OCR Only")
    print("="*60)
    
    url = f"{BASE_URL}/api/ocr/predict"
    payload = {"filename": "menu1.png"}
    
    print(f"\nSending request to: {url}")
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get('success'):
            menu_items = result.get('menu_items', [])
            print(f"\nRecognized {len(menu_items)} dishes:")
            for item in menu_items[:10]:
                print(f"   - {item.get('dish', 'N/A')}")
        else:
            print(f"\nFailed: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    print("\nStarting Menu API Tests")
    print("="*60)
    
    print("\nPlease select test:")
    print("1. OCR + Image Search (complete pipeline)")
    print("2. OCR Only")
    print("3. Run all tests")
    
    choice = input("\nEnter option (1-3): ").strip()
    
    if choice == '1':
        test_ocr_with_images()
    elif choice == '2':
        test_ocr_only()
    elif choice == '3':
        test_ocr_only()
        test_ocr_with_images()
    else:
        print("\nInvalid option, running complete pipeline test")
        test_ocr_with_images()
    
    print("\n" + "="*60)
    print("Tests completed")
    print("="*60 + "\n")
