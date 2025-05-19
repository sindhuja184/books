from fastapi import FastAPI, APIRouter, status, Depends
from pydantic import BaseModel
from typing import List
from src.books.service import BookService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from .model import chain
from langchain.prompts import PromptTemplate
from fastapi.exceptions import HTTPException
import json
from .schemas import RecommendationResponse

book_service = BookService()
rec_router = APIRouter()


@rec_router.get('/{book_uid}')
async def get_recommendations(
    book_uid: str,
    session: AsyncSession = Depends(get_session)  # ✅ Correct way
):
    book = await book_service.get_book(book_uid, session)
    book_title = book.title
    if not book:
        return HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Book Not Found"
        )


    raw_response = chain.invoke({"book_title": book_title})


    return raw_response
    

