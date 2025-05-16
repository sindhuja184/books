from pydantic import BaseModel, Field
import uuid
from src.books.schemas import Book
from datetime import datetime
from typing import List
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    first_name : str = Field(max_length= 25)
    last_name : str =  Field(max_length= 25)
    username: str = Field(max_length= 8)
    email: str = Field(max_length = 40)
    password: str = Field(max_length=20)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name:str
    is_verified: bool = Field(default=False)
    password_hash:str 
    created_at: datetime
    updated_at: datetime
    books : List[Book]
    class Config: 
        orm_mode = True

    
class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]
     
    
class UserLoginModel(BaseModel):
    email: str = Field(max_length= 40)
    password:str = Field(min_length= 6)

    
class EmailModel(BaseModel):
    addresses :List[str]
    class Config:
        from_attributes = True 