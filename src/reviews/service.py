from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status
import logging


book_service = BookService()
user_service = UserService()


class ReviewService:
    """
        Adds a review for a specific book by a specific user.

        Parameters:
        ----------
        user_email : str
            The email address of the user who is submitting the review.
        
        book_uid : str
            The unique identifier of the book being reviewed.
        
        review_data : ReviewCreateModel
            A Pydantic model containing the content of the review (e.g., rating, text).
        
        session : AsyncSession
            The asynchronous SQLAlchemy session used to interact with the database.

        Process:
        -------
        1. Retrieves the book from the database using its UID.
        2. Retrieves the user from the database using their email.
        3. Unpacks review data into a dictionary.
        4. Creates a new Review instance.
        5. Links the review to the user and book via ORM relationships.
        6. Adds and commits the new review to the database.

        Raises:
        ------
        HTTPException:
            - 500 INTERNAL_SERVER_ERROR if any part of the process fails.
    """
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession   
    ):    
        try:
            book = await book_service.get_book(
                book_uid = book_uid,
                session = session
            )

            user = await user_service.get_user_by_email(
                email= user_email,
                session= session
            )

            review_data_dict = review_data.model_dump()

            new_review = Review(
                **review_data_dict
            )

            if not book:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Book not found"
                )
            
            if not user :
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail = "User not found"
                )
            
            new_review.user = user
            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= "Something went wrong!!! Please wait"
            )