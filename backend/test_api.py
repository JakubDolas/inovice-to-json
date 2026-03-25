import requests

URL = "http://127.0.0.1:8000/api/process-invoice/"

IMAGE_PATH = "data/test3.png"

def test_ai_backend():
    print(f"Wysyłam plik {IMAGE_PATH} do serwera...")
    
    with open(IMAGE_PATH, 'rb') as f:
        files = {'invoice_image': f}
        
        response = requests.post(URL, files=files)
        
    print(f"\nStatus kod od serwera: {response.status_code}")
    print("Odpowiedź (JSON):")
    print(response.json())

if __name__ == "__main__":
    test_ai_backend()