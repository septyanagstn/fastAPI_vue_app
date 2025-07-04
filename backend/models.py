from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Article(BaseModel):
    title: str
    author: str
    post_date: datetime
    content: str
    thumbnail: str

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    disabled: bool = False

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None