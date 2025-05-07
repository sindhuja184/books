## JWT Authentication (HTTP Bearer Authentication)
# HTTP Bearer token authentication.

#     ## Usage

#     Create an instance object and use that object as the dependency in `Depends()`.

#     The dependency result will be an `HTTPAuthorizationCredentials` object containing
#     the `scheme` and the `credentials`.

from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import Any, List
from .models import User

user_service = UserService()

#Making this the base class
class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        '''
        Calls the parent HTTPBearer constructor.

        auto_error=True means FastAPI will automatically return a 
        403 Forbidden error if the Authorization header is missing 
        or invalid.
        '''
        super().__init__(auto_error=auto_error)

    #This function is responsible for the Not authorisation error 403
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        '''
        It receives the incoming request.
        await super().__call__(request) does all the heavy lifting:
        Looks for the Authorization header.
        Parses it into an HTTPAuthorizationCredentials object.
        If the header is missing, malformed, or doesn't start with Bearer, 
        and auto_error=True, it raises:

        {
            "detail": "Not authenticated"
        }

        '''
        creds =  await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = {
                    "error": "This token is expired or invalid",
                    "resolution": "Please get a new token"
                }
            )
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= {
                    'error' : 'This token has been revoked', 
                    'resolution' : 'Please get a new token'
                }
            )
    
        self.verify_token_data(token_data)
        return token_data #get access to the user id
    

    def token_valid(self, token: str) -> bool:
        '''
        Check if the given token is valid
        This function returns true if the token is valid
        else returns false
        '''
        token_data = decode_token(token)

        return True if token_data is not None else False

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override the method in Child Classes")
    

class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = "Please provide a access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = "Please provide a refresh token"
            )


async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
    ):
    
    user_email = token_details['user']['email']

    user = await user_service.get_user_by_email(user_email, session)

    return user



class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:

        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)) -> Any:

        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = 'You are not permitted to take this action'
        )