
"""A script to test PaddleOCR with a fine-tuned recognition model on any PDF files in a specified directory."""
from pathlib import Path
from paddleocr import PaddleOCR


# Use your fine‑tuned recognition model
ocr = PaddleOCR(
    text_recognition_model_dir="PaddleOCR/PP-OCRv5_server_rec_infer"
)


pdf_dir = Path("model-test-pdfs")
out_root = Path("model-test-output")
out_root.mkdir(exist_ok=True)

for pdf in sorted(pdf_dir.glob("*.pdf")):
    print(f"PDF: {pdf.name}")
    results = ocr.predict(str(pdf))
    for page_idx, res in enumerate(results, 1):
        page_dir = out_root / pdf.stem / f"page_{page_idx}"
        page_dir.mkdir(parents=True, exist_ok=True)
        res.save_to_img(str(page_dir))
        res.save_to_json(str(page_dir))
print("Done.")