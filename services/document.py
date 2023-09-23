import mimetypes
from typing import Optional, List

import structlog
from langchain.schema import Document

log = structlog.stdlib.get_logger("service.file")


def get_mimetype(filepath: str):
    mimetype, _ = mimetypes.guess_type(filepath)
    if not mimetype:
        if filepath.endswith(".md"):
            mimetype = "text/markdown"
        else:
            raise Exception("Unsupported file type")
    return mimetype


def extract_from_file(filepath: str, mimetype: Optional[str] = None) -> List[Document]:
    if not mimetype:
        mimetype = get_mimetype(filepath)
    documents = []
    if mimetype == "application/pdf":
        from langchain.document_loaders.pdf import PDFPlumberLoader

        loader = PDFPlumberLoader(filepath)
        
        documents = loader.load()

    elif mimetype == "text/plain" or mimetype == "text/markdown":
        with open(filepath, "r") as file:
            documents = [
                Document(
                    page_content=file.read().decode("utf-8"),
                    metadata={}
                )
            ]

    elif mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise NotImplementedError("DOCX not implemented")
    elif mimetype == "text/csv":
        raise NotImplementedError("CSV not implemented")
    elif mimetype == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        raise NotImplementedError("PPTX not implemented")
    else:
        raise ValueError("Unsupported file type: {}".format(mimetype))
    
    return documents

