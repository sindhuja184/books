from fastapi import FastAPI
from src.books.routes import router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from fastapi import status
from fastapi.responses import JSONResponse

from .errors import (
    create_exception_handler,
    InvalidToken,
    RevokedToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    UserAlreadyExists,
    TagAlreadyExists,
    InvalidCredentials,
    InsufficientPermission,
    BookNotFound,
    TagNotFound,
    UserNotFound,
    ExpiredToken
)

version = 'v1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The server is starting..")
    from src.db.models import Book
    
    await init_db()
    yield
    print("The server has been stopped")

app = FastAPI(
    title= "Bookly",
    description = 'A REST API for a book review and web service',
    version= version
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User is trying to login with invalid creds",
            "error_code": "Invalid Credentials"
        }
    )
)
app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User is using revoked token",
            "error_code": "revoke token"
        }
    )
)
app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code= status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Access Token Required",
            "error_code": "access token required"
        }
    )
)
app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code= status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Refresh Token Required",
            "error_code": "refresh token required"
        }
    )
)
app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with this email already exists",
            "error_code": "user exists"
        }
    )
)
app.add_exception_handler(
    TagAlreadyExists,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Tag already exists",
            "error_code": "tag exists"
        }
    )
)
app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code= status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid credentials",
            "error_code": "invalid credentials"
        }
    )
)
app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code= status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "You donot have access to this section",
            "error_code": "access denied"
        }
    )
)
app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code= status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book Not Found",
            "error_code": "book not found"
        }
    )
)
app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code= status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Tag Not Found",
            "error_code": "tag not found"
        }
    )
)
app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with this email already exists",
            "error_code": "user exists"
        }
    )
)
app.add_exception_handler(
    ExpiredToken,
    create_exception_handler(
        status_code= status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token has expired",
            "error_code": "token expired"
        }
    )
)

@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content = {
            "message":"Oops something went wrong", 
            "error_code": "server_error"
        },
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
    )
app.include_router(router=router, prefix=f'/api/{version}/books')
app.include_router(router = auth_router, prefix = f'/api/{version}/auth')
app.include_router(review_router, prefix= f'/api/{version}/reviews')
app.include_router(tags_router, prefix= f'/api/{version}/tags')