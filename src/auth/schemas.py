from pydantic import BaseModel, Field, EmailStr
import uuid 
from datetime import datetime
class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: EmailStr = Field(max_length=40)
    password: str= Field(min_length=6)
    fname:str
    lname:str
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username:str
    email:str
    fname:str
    lname:str
    is_verified:bool
    password_hash:str = Field(exclude=True)
    created_at:datetime
    update_at:datetime


class UserLoginModel(BaseModel):
    # uid: uuid.UUID
    email: EmailStr = Field(max_length=40)
    password: str= Field(min_length=6)
    # password_hash:str = Field(exclude=True)