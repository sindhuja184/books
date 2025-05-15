from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse

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