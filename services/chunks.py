import uuid
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel

from schema.models import Document
from schema.models import DocumentChunk
from schema.models import DocumentChunkMetadata
from services.embedding import get_document_embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChunkConfig(BaseModel):
    size: Optional[int] = 350        # The number of tokens in each chunk
    overlap: Optional[int] = 100     # The number of tokens to overlap between chunks


def get_text_chunks(
    text: str, 
    config: Optional[ChunkConfig] = None
) -> List[str]:
    """Transfrom text into a list of chunks."""
    if not text or text.isspace():
        return []

    if config is None:
        config = ChunkConfig()
    spliter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        separators=[r"\n\n*", r"\n", " "],
        chunk_size=config.size, 
        chunk_overlap=config.overlap
    )
    chunks = spliter.create_documents([text])
    chunks = [chunk.page_content for chunk in chunks]
    return chunks


def create_document_chunks(
    doc: Document, 
    config: Optional[ChunkConfig] = None
) -> Tuple[List[DocumentChunk], str]:
    """
    Convert a document into a list of document chunks without embeddings.
    """
    if not doc.text or doc.text.isspace():
        return [], doc.id or str(uuid.uuid4())
  
    # Generate a document id if not provided
    metadata = doc.metadata.dict()
    source_id = doc.id or metadata.get("section_id") or metadata.get("document_id")

    # Split the document text into chunks
    text_chunks = get_text_chunks(doc.text, config)

    metadata = (
        DocumentChunkMetadata(source_id=source_id, **doc.metadata.__dict__)
        if doc.metadata is not None
        else DocumentChunkMetadata(source_id=source_id)
    )

    doc_chunks = []
    for i, text_chunk in enumerate(text_chunks):
        chunk_id = f"{source_id}_{i}"
        doc_chunk = DocumentChunk(
            id=chunk_id,
            text=text_chunk,
            metadata=metadata,
        )
        doc_chunks.append(doc_chunk)

    return doc_chunks, source_id


async def get_document_chunks(
    documents: List[Document], 
    config: Optional[ChunkConfig] = None
) -> Dict[str, List[DocumentChunk]]:
    """
    Convert a list of documents into a dictionary 
    from source_id to list of document chunks with embeddings.
    """

    chunks: Dict[str, List[DocumentChunk]] = {}
    all_chunks: List[DocumentChunk] = []

    for doc in documents:
        doc_chunks, source_id = create_document_chunks(doc, config)
        all_chunks.extend(doc_chunks)
        chunks[source_id] = doc_chunks

    if not all_chunks:
        return {}

    # Get all the embeddings for the document chunks in batches, using get_embeddings
    embeddings = await get_document_embeddings(all_chunks)

    # Update the document chunk objects with the embeddings
    for i, chunk in enumerate(all_chunks):
        chunk.embedding = embeddings[i]

    return chunks
