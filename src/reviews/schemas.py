from pydantic import BaseModel
from datetime import date, datetime
import uuid
from sqlmodel import SQLModel, Field, Column, Relationship
from typing import TYPE_CHECKING, List, Optional
from src.db.models import User, Book


class ReviewModel(BaseModel):
    uid:uuid.UUID
    rating:int=Field(le=5)
    review_text:str
    user_id:Optional[uuid.UUID]
    book_id:Optional[uuid.UUID]
    created_at: datetime
    update_at: datetime 

class ReviewCreateModel(BaseModel):
    rating:int=Field(le=5)
    review_text:str