from fastapi import FastAPI, APIRouter, status, Depends
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
from src.books.schemas import BookCreateModel, BookUpdateModel, Book, BookDetailModel
from src.books.service import BookService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import BookNotFound

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

role_checker_admin = RoleChecker(['admin'])
role_checker_user_admin= RoleChecker(['admin', "user"])

# In the route:
#No need authentication
@router.get('/', 
            response_model=List[Book]
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    ):
    #Indicates whether this is a refresh token or an access token.
    books = await book_service.get_all_books(session)
    return books  # No need for from_orm since we now have actual Book instances


@router.get('/user/{user_uid}', 
            response_model=List[Book], 
)
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker_user_admin)
    ):

    books = await book_service.get_user_books(user_uid, session)
    return books  # No need for from_orm since we now have actual Book instances


@router.post('/', 
             status_code=status.HTTP_201_CREATED, 
             response_model= Book, 
)
async def create_a_book(
    book_data: BookCreateModel, 
    session: AsyncSession = Depends(get_session),
    token_details : dict = Depends(access_token_bearer),
    _: bool = Depends(role_checker_user_admin)
)-> dict:
    user_id = token_details.get('user')['user_uid']
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


#No need authentication
@router.get('/{book_uid}', 
            response_model = BookDetailModel,
)
async def get_book(
    book_uid:str,
    session: AsyncSession = Depends(get_session),
    # token_details : dict = Depends(access_token_bearer),
    # _: bool = Depends(role_checker_user_admin)
    ) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found")



@router.patch('/{book_uid}', 
              response_model=Book,
)
async def update_book(
    book_uid: str, 
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker_user_admin)
    ) -> dict:
    
    update_book = await book_service.update_book(book_uid, book_update_data, session)

    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.delete('/{book_uid}', 
               status_code= status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker_admin)
    ):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise BookNotFound()
    else:
        return {}
    
