from pydantic import BaseModel, Field, EmailStr
import uuid 
from datetime import datetime
from typing import List
from src.books.schemas import Book

class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: EmailStr = Field(max_length=40)
    password: str= Field(min_length=6)
    fname:str
    lname:str
    role:str
class UserModel(BaseModel):
    uid: uuid.UUID
    username:str
    email:str
    fname:str
    lname:str
    role:str
    is_verified:bool
    password_hash:str = Field(exclude=True)
    created_at:datetime
    update_at:datetime

class UserBooksModel(UserModel): 
    books:List[Book]


class UserLoginModel(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str= Field(min_length=6)


class EmailModel(BaseModel):
    addresses:list[str]