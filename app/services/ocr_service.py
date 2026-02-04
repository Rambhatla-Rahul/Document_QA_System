import easyocr
import numpy as np

reader = easyocr.Reader(['en'])
def run_ocr(images):
    results = []
    for img in images:
        img_np = np.array(img)
        text = reader.readtext(img_np, detail=0)
        results.append(" ".join(text))
    return results