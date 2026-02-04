from pathlib import Path
import fitz
from PIL import Image
import io

def extract_text_or_images(pdf_path: Path):
    if not pdf_path.exists():
        raise FileNotFoundError("PDF not found")

    doc = fitz.open(pdf_path)

    extracted_text = []
    images_for_ocr = []
    for page in doc:
        text = page.get_text().strip()
        mat = fitz.Matrix(300/72,300/72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        if text:
            extracted_text.append(text)
        if img:
            images_for_ocr.append(img)
    print(images_for_ocr)
    
    return extracted_text,images_for_ocr