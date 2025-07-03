from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    title: str
    author: str
    date: datetime.date
    content: str
    thumbnail: str

class User(BaseModel):
    username: str
    email: str
    password: str