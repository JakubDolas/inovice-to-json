import json
import easyocr
from groq import Groq

class InvoiceExtractor:
    def __init__(self, groq_api_key):
        print("   [System] Ładowanie modeli OCR i AI...")
        self.reader = easyocr.Reader(['pl'], gpu=False)
        self.client = Groq(api_key=groq_api_key)

    def extract_data(self, processed_path):
        """Faza 2: OCR + NLP (Ekstrakcja i JSON)"""
        print("[OCR] Analizowanie tekstu z obrazu...")
        results = self.reader.readtext(processed_path, detail=0)
        print(f"\n Wynik OCR: {results}")
        raw_text = " ".join(results)

        if not raw_text.strip():
            return {"error": "Brak tekstu na zdjęciu"}

        print("[LLM] Ustrukturyzowanie danych do JSON...")
        chat = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "Jesteś parserem faktur. Zwróć JSON z polami: 'nr_faktury', 'sprzedawca_nip', 'nabywca_nip', 'total_brutto' (float)."
                },
                {"role": "user", "content": f"Tekst: {raw_text}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(chat.choices[0].message.content)