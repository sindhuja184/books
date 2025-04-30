#Faced an error that password hash field was'nt there 
#Has to fix the signup logic  as it created issues
# Has to change the type of timedelta for expiry 
# it created an issue as its not json serialoisablle 


from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()


REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
        '/signup', 
        response_model= UserModel,
        status_code= status.HTTP_201_CREATED
    )
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
    ):    
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "User with the email already exists")
    
    new_user = await user_service.create_user(
        user_data,
        session
    )

    return new_user



@auth_router.post('/login')
async def login_users(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        #  Access Token:
        # Purpose: Used to access protected routes or resources.

        # Short-lived: Typically valid for a short time (e.g., 15 minutes to 1 hour).

        # Sent with each request: Clients send it in the header (Authorization: Bearer <token>) to prove they are authenticated.

        # Smaller risk: Since it expires quickly, even if stolen, damage is limited.

        # Refresh Token:
        # Purpose: Used to get a new access token without logging in again.

        # Long-lived: Can last days, weeks, or more.

        # Stored securely: Should not be sent with every request—store it securely (e.g., HTTP-only cookie).

        # Used when access token expires: Client sends it to the server to request a new access token.
        if password_valid:
            access_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'user_uid' : str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'user_uid' : str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY).total_seconds()  # **Convert timedelta to seconds**
            )

            return JSONResponse(
                content= {
                    "message": "Login Sucessful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Invalid Email or Password"
        )

