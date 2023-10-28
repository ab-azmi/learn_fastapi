
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    

class ResponsePost(Post):
    id: int
    created_at: datetime

    #turn model into dict
    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #turn model into dict
    class Config:
        from_attributes = True