from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class BooklyException(Exception):
    '''Base class for all the bookly errors'''
    
class InvalidToken(BooklyException):
    '''User provided an invalid token or expired token'''
    pass
    
class RevokedToken(BooklyException):
    '''User provided a tken that has been revoked'''
    pass
    
class AccessTokenRequired(BooklyException):
    '''User provided a refresh token when access token is needed'''
    pass
    
class RefreshTokenRequired(BooklyException):
    '''User provided a access token when refresh token is required'''
    pass

class UserAlreadyExists(BooklyException):
    '''User has provided an access token when refresh token is required'''
    pass

class TagAlreadyExists(BooklyException):
    '''Tag already exists'''
    pass


class InvalidCredentials(BooklyException):
    '''User provided wrong credentials during log in'''
    pass

class InsufficientPermission(BooklyException):
    '''User does not have neccessary permissions to perform this action'''
    pass

class BookNotFound(BooklyException):
    '''Book Not Found!!!'''
    pass

class TagNotFound(BooklyException):
    '''Tag Not Found!!!'''
    pass

class UserNotFound(BooklyException):
    '''User Not Found!!!'''
    pass

class ExpiredToken(BooklyException):
    '''Invalid or expired token'''



def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    
    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(
            content = initial_detail,
            status_code= status_code
        )
    
    return exception_handler

def register_all_errors(app: FastAPI):
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
    
    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))
        return JSONResponse(
            content= {
                "message" : "ops something went wrong",
                "error_code": "server_error"
            },
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
        )