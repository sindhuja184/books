from pydantic import BaseModel
from datetime import datetime, date
from typing import List
import uuid
from src.reviews.schemas import ReviewModel

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author:  str
    publisher:  str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BookDetailModel(Book):
    reviews: List[ReviewModel]
    
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher:str
    page_count: int
    language: str