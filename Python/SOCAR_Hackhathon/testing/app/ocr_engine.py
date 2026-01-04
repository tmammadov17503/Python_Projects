import cv2
import numpy as np
import pytesseract
from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
import os
import re


class OCREngine:
    def __init__(self):
        print("Initializing OCR Engines (Dictionary Rescue Mode)...")

        # 1. PaddleOCR
        self.ocr_lat = PaddleOCR(lang='en', use_angle_cls=False)
        self.ocr_cyr = PaddleOCR(lang='ru', use_angle_cls=False)

        # 2. Tesseract Setup
        self.use_tesseract = False

        # DOMAIN DICTIONARY: These words are "VIPs". We always keep them.
        self.socar_keywords = [
            "aymt", "mq", "alt", "horizont", "quyu", "sahə", "dərinlik", "neft", "qaz",
            "seysmik", "geofizika", "profil", "zaman", "metr", "il", "area", "well",
            "depth", "seismic", "time", "fig", "table", "şəkil", "abşeron", "kür", "bakı"
        ]

        tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(tess_path):
            tess_path = r'C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        if os.path.exists(tess_path):
            pytesseract.pytesseract.tesseract_cmd = tess_path
            self.use_tesseract = True
            print("✅ Tesseract READY.")
        else:
            print("⚠️ Tesseract NOT found.")

    def clean_seismic_noise(self, img_gray):
        # 1. Threshold
        thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        # 2. Open (Remove small dots)
        kernel = np.ones((2, 2), np.uint8)
        clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        return clean

    def extract_smart_text(self, img_np, lang_str):
        """
        Extracts text using a hybrid logic:
        Keep High Confidence Words OR Domain Keywords.
        """
        # Preprocess
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        clean = self.clean_seismic_noise(gray)

        # Get Data (Word by Word analysis)
        config = r'--oem 3 --psm 11'
        data = pytesseract.image_to_data(clean, lang=lang_str, config=config, output_type=pytesseract.Output.DICT)

        kept_words = []
        n_boxes = len(data['text'])

        for i in range(n_boxes):
            word = data['text'][i].strip()
            if not word: continue

            conf = int(data['conf'][i])
            word_lower = word.lower()

            # --- THE DECISION LOGIC ---

            # 1. Is it a Keyword? (Keep even if confidence is low, e.g. 30%)
            is_keyword = any(k in word_lower for k in self.socar_keywords)

            # 2. Is it a Number? (Keep if confidence is decent > 40%)
            is_number = bool(re.search(r'\d', word))

            # 3. Is it High Confidence Text? (Keep if > 60%)
            is_clear_text = conf > 60 and len(word) > 2

            # 4. Filter out obvious map noise (single random chars like 't', 'r', '_')
            if len(word) < 2 and not is_number:
                continue

            if is_keyword or (is_number and conf > 40) or is_clear_text:
                kept_words.append(word)

        return " ".join(kept_words)

    def process_pdf(self, pdf_bytes: bytes, mode: str = "auto") -> list:
        # DPI=200
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

                # 1. Standard Paddle Run
                engine = self.ocr_cyr if mode == "cyr" else self.ocr_lat

                # Resize check
                h, w = img_np.shape[:2]
                if w > 2500:
                    scale = 2500 / w
                    img_paddle = cv2.resize(img_np, None, fx=scale, fy=scale)
                else:
                    img_paddle = img_np

                ocr_result = engine.ocr(img_paddle)
                md_text = self._parse_result_deep(ocr_result)

                # 2. Map Detection
                is_weak = len(md_text.strip()) < 30

                if is_weak and self.use_tesseract:
                    print(f"  > Map detected. Running DICTIONARY RESCUE...")

                    lang_str = "aze+eng" if mode == "lat" else "aze_cyrl+rus+eng"

                    # 3. Run Smart Extraction
                    smart_text = self.extract_smart_text(img_np, lang_str)

                    if len(smart_text) > 5:
                        md_text = f"## EXTRACTED MAP DATA:\n{smart_text}"
                    else:
                        md_text = "EMPTY (No Recognizable Data Found)"

                results.append({"page_number": page_num, "MD_text": md_text})

                preview = md_text[:100].replace('\n', ' ') if md_text else "EMPTY"
                print(f"  > Final: {preview}...")

            except Exception as e:
                print(f"ERROR on page {page_num}: {e}")
                results.append({"page_number": page_num, "MD_text": ""})

        return results

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