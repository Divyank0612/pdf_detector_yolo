import os
import cv2
import fitz  # PyMuPDF for PDF reading
import torch
import pytesseract
import numpy as np
from PIL import Image
from ultralytics import YOLO

# Load YOLOv10 pretrained model (already fine-tuned on DocLayNet)
MODEL_PATH = "models/yolov10_doclaynet.pt"
model = YOLO(MODEL_PATH)

# OCR config
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Class names as per DocLayNet
CLASS_NAMES = ["Caption", "Footnote", "Formula", "List-item", "Page-footer", 
               "Page-header", "Picture", "Section-header", "Table", "Text"]

def verify_with_ocr(image, bbox, label):
    """
    Cross-check detection with OCR/textual clues.
    bbox = [x1, y1, x2, y2]
    """
    x1, y1, x2, y2 = map(int, bbox)
    crop = image[y1:y2, x1:x2]

    # OCR result
    ocr_text = pytesseract.image_to_string(crop).strip()

    # Heuristic checks
    if label == "Table" and ("|" in ocr_text or "\t" in ocr_text):
        return True
    if label == "Equation" and any(ch in ocr_text for ch in ["=", "+", "-", "/", "*"]):
        return True
    if label == "Section-header" and len(ocr_text.split()) < 6:
        return True
    if label == "Text" and len(ocr_text.split()) > 6:
        return True

    # If OCR gives no meaningful text, reject questionable "Text" label
    if label == "Text" and ocr_text == "":
        return False

    # Default: trust YOLO prediction
    return True

def process_pdf(pdf_path, output_dir="outputs_hybrid/"):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        if pix.n == 4:  # RGBA → RGB
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        # Run YOLO detection
        results = model(img)

        annotated = img.copy()
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = CLASS_NAMES[cls_id]
                conf = float(box.conf[0])
                bbox = box.xyxy[0].cpu().numpy()

                # OCR verification
                is_valid = verify_with_ocr(img, bbox, label)

                if is_valid:
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated, f"{label} {conf:.2f}", 
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                                0.6, (0, 255, 0), 2)

        out_path = os.path.join(output_dir, f"page_{page_num+1}.png")
        cv2.imwrite(out_path, annotated)
        print(f"Saved annotated page {page_num+1} → {out_path}")

if __name__ == "__main__":
    process_pdf("Workbook.pdf")
