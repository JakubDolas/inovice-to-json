import os
import cv2

class ImagePreprocessor:
    def __init__(self, output_dir="data/processed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_invoice(self, image_path):
        print("[OpenCV] Optymalizacja obrazu pod OCR...")
        img = cv2.imread(image_path)
        
        if img is None:
            raise FileNotFoundError(f"Nie znaleziono pliku wejściowego: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )

        processed_path = os.path.join(self.output_dir, "cleaned_invoice.jpg")
        cv2.imwrite(processed_path, binary)
        return processed_path