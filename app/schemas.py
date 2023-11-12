
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    

class ResponsePost(Post):
    id: int
    created_at: datetime
    owner_id: int

    #turn model into dict
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #turn model into dict
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None