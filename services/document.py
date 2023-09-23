import time
import mimetypes
import tempfile
import logging
from typing import Optional, List

import structlog
from fastapi import UploadFile
from langchain.schema import Document as LangchainDocument

from schema.models import Document
from schema.models import DocumentMetadata

log = structlog.stdlib.get_logger("service.file")

async def get_documents_from_upload_file(file: UploadFile, metadata: DocumentMetadata):
    output = []
    documents = await extract_from_upload_file(file)
    for i, doc in enumerate(documents):
        meta = metadata.dict()
        other = doc.metadata
        if metadata.other:
            other.update(**metadata.other.dict())
        meta["other"] = other
        output.append(
            Document(
                id=f"{metadata.document_id}_{i}",  # need a unique source_id for each chunk batch
                text=doc.page_content,
                metadata=meta,
            )
        )
    return output

async def get_documents_from_file(filepath: str, metadata: DocumentMetadata):
    output = []
    documents = extract_from_file(filepath)
    print(documents)
    for i, doc in enumerate(documents):
        meta = metadata.dict()
        other = doc.metadata
        if metadata.other:
            other.update(**metadata.other.dict())
        meta["other"] = other
        output.append(
            Document(
                id=f"{metadata.document_id}_{i}",  # need a unique source_id for each chunk batch
                text=doc.page_content,
                metadata=meta,
            )
        )
    return output

def get_mimetype(filepath: str):
    mimetype, _ = mimetypes.guess_type(filepath)
    if not mimetype:
        if filepath.endswith(".md"):
            mimetype = "text/markdown"
        else:
            raise Exception("Unsupported file type")
    return mimetype


def extract_from_file(filepath: str, mimetype: Optional[str] = None) -> List[LangchainDocument]:
    if not mimetype:
        mimetype = get_mimetype(filepath)
    documents = []
    if mimetype == "application/pdf":
        from langchain.document_loaders.pdf import PDFPlumberLoader
        #from langchain.document_loaders.pdf import UnstructuredPDFLoader

        loader = PDFPlumberLoader(filepath)
        
        documents = loader.load()

    elif mimetype == "text/plain" or mimetype == "text/markdown":
        with open(filepath, "r") as file:
            documents = [
                LangchainDocument(
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


async def extract_from_upload_file(file: UploadFile) -> List[LangchainDocument]:
    mimetype = file.content_type
    start = time.time()
    log.info(
        f"Extracting text from file: {file.filename}",
        data={"mimetype": mimetype, "filename": file.filename, "size": file.size},
    )
    file_data = await file.read()
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(file_data)
        documents = extract_from_file(temp_file.name, mimetype)
    log.info(
        "Finished extracting text from file", 
        data={ "time": time.time() - start, "filename": file.filename, "documents": len(documents) }
    )
    return documents
