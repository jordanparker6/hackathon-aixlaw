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
