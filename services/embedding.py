from typing import List
import structlog
import tenacity

from schema.models import DocumentChunk
from langchain.embeddings import OpenAIEmbeddings

log = structlog.stdlib.get_logger("service.embedding")

DOCUMENT_EMBEDING_TEMPLATE = """
DOCUMENT TITLE: {document_title}
SECTION TITLE: {section_title}
JURISDICTION: {jurisdiction}
INSTRUMENT: {instrument}
---
{text}
"""

@tenacity.retry(wait=tenacity.wait_exponential(min=10, max=60), stop=tenacity.stop_after_attempt(3))
async def get_document_embeddings(chunks: List[DocumentChunk]) -> List[List[float]]:
    texts = [
        DOCUMENT_EMBEDING_TEMPLATE.format(**{ 
            "text": chunk.text, 
            "document_title": chunk.metadata.document_title, 
            "section_title": chunk.metadata.section_title, 
            "instrument": chunk.metadata.instrument,
            "jurisdiction": chunk.metadata.jurisdiction,
        }) for chunk in chunks
    ]
    model = OpenAIEmbeddings(model="text-embedding-ada-002")
    embeddings = await model.aembed_documents(texts)
    return embeddings

async def get_query_embeddings(text: List[str]) -> List[List[float]]:
    model = OpenAIEmbeddings(model="text-embedding-ada-002")
    embeddings = await model.embed_query(text)
    return embeddings
