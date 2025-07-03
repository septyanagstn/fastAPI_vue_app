from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    title: str
    author: str
    post_date: datetime
    content: str
    thumbnail: str

class User(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    disabled: bool = False

class TokenData(BaseModel):
    access_token: str
    token_type: str