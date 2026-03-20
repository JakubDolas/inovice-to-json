# Reading data from an invoice to JSON

System ML do automatycznego pobierania danych z faktur. System zamienia surowe zdjęcia dokumentów w ustrukturyzowane obiekty JSON, łącząc Computer Vision z modelami LLM.

1. **Wizja (OpenCV):** Oczyszcza skan i podbija kontrast przygotowując go pod OCR.
2. **Ekstrakcja (EasyOCR):** Odczytuje surowy tekst z przygotowanego obrazu.
3. **Rozumowanie (Groq API):** Analizuje teskt i wyciąga konkretne dane do formatu JSON.
4. **Walidacja (QA):** Porównuje wynik z wzorcem i na wylicza skuteczność.

```bash
# 1. Pobierz repozytorium
cd invoice-to-json

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Skonfiguruj klucz API
# W pliku .env wklej swój klucz:
# GROQ_API_KEY=twoj_klucz_api_tutaj

# 4. Uruchom system
python main.py
