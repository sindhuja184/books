from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

@app.get('/')
async def read_root():
    return {"message" : "hello"}

@app.get('/greet/{name}')
async def greet_name(name:Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"HEllo {name} age{age}"}
 
class BookCreateModel(BaseModel):
    title: str
    author: str

@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        "title":book_data.title,
        "author": book_data.author
    }

@app.get('/get_headers', status_code = 200)
async  def get_header(
    accept: Optional[str] = Header(None),
    content_type: str = Header(None),
    user_agent : str = Header(None),
    host : str = Header(None)
):
    request_header = {}
    request_header["Accept"] = accept
    request_header["Content-Type"] = content_type
    request_header["User-Agent"] = user_agent
    request_header["Host"] = host
    return request_header


