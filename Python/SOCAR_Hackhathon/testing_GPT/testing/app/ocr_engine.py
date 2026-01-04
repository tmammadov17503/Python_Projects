import cv2
import numpy as np
import pytesseract
try:
    from paddleocr import PaddleOCR
    _PADDLE_ERR = None
except Exception as e:
    PaddleOCR = None
    _PADDLE_ERR = str(e)

from pdf2image import convert_from_bytes
import os
import re


class OCREngine:
    def __init__(self):
        print("Initializing OCR Engines (Seismic Blob Detection Mode)...")

        # 1) PaddleOCR (optional; don't let it crash the app)
        if PaddleOCR is None:
            print(f"⚠️ PaddleOCR disabled (import failed): {_PADDLE_ERR}")
            self.ocr_lat = None
            self.ocr_cyr = None
        else:
            try:
                self.ocr_lat = PaddleOCR(lang='en', use_angle_cls=False)
                self.ocr_cyr = PaddleOCR(lang='ru', use_angle_cls=False)
                print("✅ PaddleOCR READY.")
            except Exception as e:
                print(f"⚠️ PaddleOCR init failed: {e}")
                self.ocr_lat = None
                self.ocr_cyr = None

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

    def preprocess_text_page(self, gray):
        # upscale (helps small italic text)
        gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

        # denoise
        gray = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

        # illumination correction (remove yellow paper background)
        bg = cv2.medianBlur(gray, 31)
        norm = cv2.divide(gray, bg, scale=255)

        # boost local contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        norm = clahe.apply(norm)

        # adaptive threshold
        th = cv2.adaptiveThreshold(
            norm, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35, 15
        )

        # remove horizontal notebook lines
        horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 1))
        horiz = cv2.morphologyEx(th, cv2.MORPH_OPEN, horiz_kernel)
        # horiz keeps the lines as black(0). Turn them to white(255) in th:
        th[horiz == 0] = 255

        return th

    def tesseract_with_conf(self, img, lang_str, psm):
        config = f"--oem 1 --psm {psm}"
        data = pytesseract.image_to_data(img, lang=lang_str, config=config, output_type=pytesseract.Output.DICT)
        confs = []
        for c in data.get("conf", []):
            try:
                v = float(c)
                if v >= 0:
                    confs.append(v)
            except:
                pass
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        text = pytesseract.image_to_string(img, lang=lang_str, config=config)
        return text, avg_conf

    def pick_best_text(self, candidates):
        # candidates: [(text, conf), ...]
        def score(text, conf):
            t = (text or "").strip()
            letters = re.findall(r"[a-zA-ZəöüğıçşƏÖÜĞIÇŞ]", t)
            letter_ratio = (len(letters) / max(1, len(re.sub(r"\s", "", t))))
            return conf * 2.0 + letter_ratio * 100.0 + min(len(t), 500) / 50.0

        best = ("", 0.0)
        best_s = -1e9
        for text, conf in candidates:
            s = score(text, conf)
            if s > best_s:
                best_s = s
                best = (text, conf)
        return best

    def process_pdf(self, pdf_bytes: bytes, mode: str = "lat") -> list:
        # DPI=200 is optimal for Tesseract speed/accuracy
        images = convert_from_bytes(
            pdf_bytes,
            dpi=300,
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
                md_text = ""

                if self.ocr_lat is not None:
                    engine = self.ocr_cyr if mode == "cyr" else self.ocr_lat
                    try:
                        ocr_result = engine.ocr(img_np)
                        md_text = self._parse_result_deep(ocr_result)
                    except Exception as e:
                        print(f"  > PaddleOCR failed on page {page_num}: {e}")
                        md_text = ""
                else:
                    # PaddleOCR disabled; we'll rely on Tesseract fallback below
                    md_text = ""

                # 3. Check for Garbage (Seismic Lines misread as text)
                clean_sample = re.sub(r'[\s0-9]', '', md_text)
                if len(clean_sample) > 0:
                    garbage_ratio = 1.0 - (len(re.findall(r'[a-zA-ZəöüğıçşƏÖÜĞIÇŞ]', clean_sample)) / len(clean_sample))
                else:
                    garbage_ratio = 0.0

                is_weak = len(md_text.strip()) < 50

                # 4. Fallback: Seismic Map Processor
                # 4) Fallback (TEXT pages first, blob isolation last)
                if (is_weak or garbage_ratio > 0.4) and self.use_tesseract:

                    # Choose language safely
                    if mode == "cyr":
                        lang_str = "aze_cyrl+rus+eng" if "aze_cyrl" in self.langs_available else "rus+eng"
                    else:
                        lang_str = "aze+eng" if "aze" in self.langs_available else "eng"

                    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

                    # ---- A) TEXT-PAGE preprocessing + best-PSM selection ----
                    th = self.preprocess_text_page(gray)

                    candidates = []
                    for psm in (6, 4, 3):
                        txt, conf = self.tesseract_with_conf(th, lang_str, psm)
                        candidates.append((txt, conf))

                    best_txt, best_conf = self.pick_best_text(candidates)
                    md_text = best_txt
                    print(f"  > Tesseract(TEXT) best avg_conf={best_conf:.1f} (lang={lang_str})")

                    # ---- B) Only if still weak: try blob isolation as LAST resort ----
                    if len(md_text.strip()) < 60:
                        print("  > Still weak. Trying Blob Isolation (last resort)...")
                        cleaned_img = self.isolate_text_regions(gray)

                        # IMPORTANT: no whitelist while debugging (whitelist often hurts OCR)
                        txt2, conf2 = self.tesseract_with_conf(cleaned_img, lang_str, 11)

                        # Keep whichever is better
                        if conf2 > best_conf and len(txt2.strip()) > len(md_text.strip()):
                            md_text = txt2
                            print(f"  > Blob Isolation improved avg_conf={conf2:.1f}")

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