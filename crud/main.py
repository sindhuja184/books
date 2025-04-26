from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
from .schemas import Book, BookUpdateModel
books = [
  {
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "author": "J.K. Rowling",
    "publisher": "Bloomsbury",
    "published_date": "1997-06-26",
    "page_count": 223,
    "language": "en"
  },
  {
    "id": 2,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "publisher": "George Allen & Unwin",
    "published_date": "1937-09-21",
    "page_count": 310,
    "language": "en"
  },
  {
    "id": 3,
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "publisher": "HarperTorch",
    "published_date": "1988-04-15",
    "page_count": 208,
    "language": "en"
  },
  {
    "id": 4,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "publisher": "J.B. Lippincott & Co.",
    "published_date": "1960-07-11",
    "page_count": 281,
    "language": "en"
  },
  {
    "id": 5,
    "title": "1984",
    "author": "George Orwell",
    "publisher": "Secker & Warburg",
    "published_date": "1949-06-08",
    "page_count": 328,
    "language": "en"
  }
]


app = FastAPI()



@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books

@app.post('/books')
async def create_a_book(book_data: Book, status_code = status.HTTP_201_CREATED):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get('/book/{book_id}')
async def get_book(book_id:int)-> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found")

@app.put('/book/{book_id}')
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

@app.delete('/book/{book_id}')
async def delete_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message": f"Book with id {book_id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

