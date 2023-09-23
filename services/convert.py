import fitz  # PyMuPDF
import os
import pdf2image
from pathlib import Path

def pdf_to_images(file: Path):
    with open(file, "rb") as f:
        pdf = f.read()
    images = pdf2image.convert_from_bytes(
        pdf,
        dpi=300,
        thread_count=os.cpu_count() if os.cpu_count() <= 4 else 4,
        fmt="png",
    )
    return images

def pdf_to_markdown(pdf_file):
    doc = fitz.open(pdf_file)
    markdown_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        markdown_text += page.get_text("text")

    return markdown_text