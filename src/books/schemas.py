from pydantic import BaseModel
from datetime import datetime


from typing import List
import uuid
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author:  str
    publisher:  str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: set
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher:str
    published_date:str
    page_count: int
    language: str