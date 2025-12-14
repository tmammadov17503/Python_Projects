import cv2
import numpy as np
import pytesseract
from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
import os
import re


class OCREngine:
    def __init__(self):
        print("Initializing OCR Engines (Final Stable Mode)...")

        # 1. PaddleOCR (Standard)
        # We use 'en' and 'ru' base models.
        self.ocr_lat = PaddleOCR(lang='en', use_angle_cls=False)
        self.ocr_cyr = PaddleOCR(lang='ru', use_angle_cls=False)

        # 2. Tesseract Setup
        self.use_tesseract = False
        self.langs_available = []

        # Check Paths (Program Files or AppData)
        tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(tess_path):
            tess_path = r'C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        if os.path.exists(tess_path):
            pytesseract.pytesseract.tesseract_cmd = tess_path
            self.use_tesseract = True

            # Detect Languages
            tessdata_path = os.path.join(os.path.dirname(tess_path), 'tessdata')
            if os.path.exists(os.path.join(tessdata_path, 'aze.traineddata')): self.langs_available.append('aze')
            if os.path.exists(os.path.join(tessdata_path, 'aze_cyrl.traineddata')): self.langs_available.append(
                'aze_cyrl')
            self.langs_available.append('eng')

            print(f"✅ Tesseract READY. Languages: {self.langs_available}")
        else:
            print("⚠️ Tesseract NOT found.")

    def isolate_text_regions(self, img_gray):
        """
        Detects text blobs and masks out seismic waves.
        """
        # 1. Morphological Gradient to find edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = cv2.morphologyEx(img_gray, cv2.MORPH_GRADIENT, kernel)

        # 2. Binarize
        _, bw = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # 3. Connect horizontally (make words into solid blocks)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

        # 4. Find Contours
        contours, _ = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 5. Create Mask
        mask = np.zeros(img_gray.shape, dtype=np.uint8)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Filter: Text is usually rectangular and not too thin
            fill_ratio = cv2.contourArea(c) / (w * h)
            if w > 10 and h > 8 and fill_ratio > 0.4:
                cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

        # 6. Apply Mask (Everything outside text boxes becomes white)
        cleaned = cv2.bitwise_and(img_gray, mask)
        cleaned[mask == 0] = 255

        return cleaned

    def process_pdf(self, pdf_bytes: bytes, mode: str = "auto") -> list:
        # DPI=200 is optimal for Tesseract speed/accuracy
        images = convert_from_bytes(
            pdf_bytes,
            dpi=200,
            poppler_path=r"C:\Program Files\poppler-25.12.0\Library\bin"
        )

        results = []
        for i, pil_image in enumerate(images):
            page_num = i + 1
            print(f"Processing Page {page_num}...")

            try:
                img_np = np.array(pil_image)

                # 1. Resize if huge (prevents crashes)
                h, w = img_np.shape[:2]
                if max(h, w) > 2500:
                    scale = 2500 / max(h, w)
                    img_np = cv2.resize(img_np, None, fx=scale, fy=scale)

                # 2. Try PaddleOCR first
                engine = self.ocr_cyr if mode == "cyr" else self.ocr_lat
                ocr_result = engine.ocr(img_np)
                md_text = self._parse_result_deep(ocr_result)

                # 3. Check for Garbage (Seismic Lines misread as text)
                clean_sample = re.sub(r'[\s0-9]', '', md_text)
                if len(clean_sample) > 0:
                    garbage_ratio = 1.0 - (len(re.findall(r'[a-zA-ZəöüğıçşƏÖÜĞIÇŞ]', clean_sample)) / len(clean_sample))
                else:
                    garbage_ratio = 0.0

                is_weak = len(md_text.strip()) < 50

                # 4. Fallback: Seismic Map Processor
                if (is_weak or garbage_ratio > 0.4) and self.use_tesseract:
                    print(f"  > Map detected (Garbage Ratio: {garbage_ratio:.2f}). Running Blob Isolation...")

                    lang_str = "aze+eng" if mode == "lat" else "aze_cyrl+rus+eng"

                    # Convert to Gray & Isolate Text Regions
                    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
                    cleaned_img = self.isolate_text_regions(gray)

                    # FIX: STRICT WHITELIST WITHOUT SPACES OR QUOTES
                    # This prevents the "No closing quotation" error
                    whitelist = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZəöüğıçşƏÖÜĞIÇŞ.,-:/()"
                    config = f'--oem 3 --psm 11 -c tessedit_char_whitelist={whitelist}'

                    tess_text = pytesseract.image_to_string(cleaned_img, lang=lang_str, config=config)
                    md_text = tess_text

                # 5. Final Filter
                md_text = self.filter_garbage_lines(md_text)
                results.append({"page_number": page_num, "MD_text": md_text})

                preview = md_text[:50].replace('\n', ' ') if md_text else "EMPTY"
                print(f"  > Final: {preview}...")

            except Exception as e:
                print(f"ERROR on page {page_num}: {e}")
                results.append({"page_number": page_num, "MD_text": ""})

        return results

    def filter_garbage_lines(self, text):
        valid_lines = []
        for line in text.split('\n'):
            line = line.strip()
            # Must be >3 chars and have at least 1 letter/number
            if len(line) > 3 and re.search(r'[a-zA-ZəöüğıçşƏÖÜĞIÇŞ0-9]', line):
                valid_lines.append(line)
        return "\n".join(valid_lines)

    def _parse_result_deep(self, result) -> str:
        found_text = []

        def extract_recursive(data):
            if isinstance(data, (list, tuple)):
                if len(data) == 2 and isinstance(data[0], str) and isinstance(data[1], (float, int)):
                    found_text.append(data[0])
                elif len(data) == 2 and isinstance(data[1], tuple) and isinstance(data[1][0], str):
                    found_text.append(data[1][0])
                else:
                    for item in data: extract_recursive(item)
            elif isinstance(data, dict):
                for key in ['text', 'rec_text']:
                    if key in data and isinstance(data[key], str): found_text.append(data[key])
                for value in data.values(): extract_recursive(value)

        extract_recursive(result)
        return "\n\n".join(list(dict.fromkeys(found_text)))