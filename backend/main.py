import os
import json
from dotenv import load_dotenv

from src.image_processing import ImagePreprocessor
from src.processor import InvoiceExtractor
from src.validator import run_full_validation

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TARGET_DATA = {
    "nr_faktury": "1/09/2019",
    "sprzedawca_nip": "9720002720",
    "nabywca_nip": "511825852",
    "total_brutto": 15953.1
}

def main():
    if not GROQ_API_KEY:
        print("BŁĄD: Brak klucza w pliku .env")
        return

    preprocessor = ImagePreprocessor()
    ai_extractor = InvoiceExtractor(GROQ_API_KEY)
    
    print("\n--- Rozpoczynam Przetwarzanie ---")
    
    # Poprawa obrazu
    p_img_path = preprocessor.clean_invoice("data/test3.png")
    
    ai_result = ai_extractor.extract_data(p_img_path)
    print("\n[TARGET DATA]: ", TARGET_DATA)
    print("\n[AI Output]:", json.dumps(ai_result, indent=2))
    
    # Ocena skuteczności
    run_full_validation(ai_result, TARGET_DATA)

if __name__ == "__main__":
    main()