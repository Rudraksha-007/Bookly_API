from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: Optional[datetime]
    page_count: int
    language: str
    created_at:datetime
    update_at:datetime
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str # type: ignore
    page_count: int
    language: str
    published_date: Optional[datetime]

class BookUpdateModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_date: Optional[datetime]
    page_count: Optional[int]
    language: Optional[str]
