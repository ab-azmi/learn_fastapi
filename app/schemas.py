
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

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

class Post(BaseModel):
    title: str
    content: str
    published: bool=True

class ResponsePost(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    #turn model into dict
    class Config:
        from_attributes = True

class PostVote(BaseModel):
    Post: ResponsePost
    votes: int

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)