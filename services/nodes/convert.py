import io
import logging
import os
from typing import List, Tuple

import fsspec
import pdf2image
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from contractron.nodes.base import BaseNodeComponent
from contractron.schema import Document
from contractron.schema import Page
from contractron.schema import StateDict


logger = logging.getLogger(__name__)


class DocumentConverter(BaseNodeComponent):
    """
    Convert a PDF Document to a list of Pages
    """

    def __init__(
        self,
        save_images: bool = False,
        dpi=300,
        image_format: str = "jpeg",
    ):
        super().__init__()
        self.save_images = save_images
        self.dpi = dpi
        self.image_format = image_format

    def model_fn(self, model_dir):
        pass

    def predict_fn(self, input_data: StateDict, model):
        documents = input_data["documents"]
        pages = []
        for doc in documents:
            pages.append(self.convert(doc))
        return {
            "documents": documents,
            "pages": pages,
        }

    def convert(self, document: Document) -> List[Page]:  # type: ignore
        """Convert a Document object to a list of Pages"""
        if document.content_type == "application/pdf":
            return self._pdf_to_pages(document, self.image_format)
        else:
            raise ValueError(f"Unsupported content type: {document.content_type}")

    def _pdf_to_pages(self, document: Document, fmt: str) -> List[Page]:
        """Converts a PDF to a collection of Pages"""
        pdf = document.content
        number, sizes = get_pdf_pages_and_sizes(pdf)

        images = pdf2image.convert_from_bytes(
            document.content,
            dpi=self.dpi,
            thread_count=os.cpu_count() if os.cpu_count() <= 4 else 4,
            fmt=fmt,
        )
        pages = []
        for i, (size, image) in enumerate(zip(sizes, images)):
            page = Page(
                document_id=document.id,
                image=image,
                number=i,
                meta={
                    "image_width": image.width,
                    "image_height": image.height,
                    "image_format": fmt,
                    "pdf_width": size[0],
                    "pdf_height": size[1],
                    "scale": [size[0] / image.width, size[1] / image.height],
                },
            )
            if self.save_images:
                uri = document.file_path
                if "://" not in uri:
                    uri = "file://" + uri
                protocol, path = uri.split("://", 1)
                _dir = f"{protocol}://" + os.path.dirname(path)
                page.meta["image_path"] = f"{_dir}/images/{page.id}.{fmt}"
                with fsspec.open(page.meta["image_path"], "wb") as f:
                    image.save(f, format=fmt)
            pages.append(page)
        return pages


def get_pdf_pages_and_sizes(pdf: bytes) -> Tuple[int, List[Tuple[int, int]]]:
    """Ref https://stackoverflow.com/a/47686921"""
    parser = PDFParser(io.BytesIO(pdf))
    document = PDFDocument(parser)
    num_pages = resolve1(document.catalog["Pages"])["Count"]
    page_sizes = [
        (int(page.mediabox[2]), int(page.mediabox[3])) for page in PDFPage.create_pages(document)
    ]
    return num_pages, page_sizes


# def _is_scanned(self, pdf: bytes) -> bool:
#     """Ref https://stackoverflow.com/questions/55704218/how-to-check-if-pdf-is-scanned-image-or-contains-text"""
#     with pdfplumber.open(file_name) as pdf:
#         page = pdf.pages[0]
#         text = page.extract_text()
#         print(text)