from pydantic import BaseModel
from typing import Optional,List
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: Optional[str]="NA"
    page_count: int
    language: str
class Bookupdate(BaseModel):
    publisher: str
    published_date: str
    page_count: int
    language: str
