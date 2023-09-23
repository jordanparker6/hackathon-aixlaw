from pydantic import BaseModel
from typing import Optional

class DocumentMetadata:
    id: Optional[str] = None
    chunk_id: Optional[str] = None
    title: Optional[str] = None
    
