from fastapi import FastAPI, APIRouter, status
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
from ..books.schemas import Book, BookUpdateModel
from .book_data import books
router = APIRouter()

@router.get('/', response_model=List[Book])
async def get_all_books():
    return books

@router.post('/')
async def create_a_book(book_data: Book, status_code = status.HTTP_201_CREATED):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@router.get('/{book_id}')
async def get_book(book_id:int)-> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found")

@router.put('/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author           # <-- Add this
            book['publisher'] = book_update_data.publisher
            book['published_date'] = book_update_data.published_date  # <-- Add this
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@router.delete('/{book_id}')
async def delete_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message": f"Book with id {book_id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

