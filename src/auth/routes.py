#Faced an error that password hash field was'nt there 
#Has to fix the signup logic  as it created issues
# Has to change the type of timedelta for expiry 
# it created an issue as its not json serialoisablle 


from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from datetime import datetime
from src.db.redis import add_jti_to_blacklist
from src.errors import UserAlreadyExists, UserNotFound, InvalidCredentials, ExpiredToken



auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', "user"])


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
    """
    Create user account using email, username, first_name, last_name
    params:
        user_data: UserCreateModel
    """
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()
    
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

        if password_valid:
            access_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'user_uid' : str(user.uid),
                    'role': user.role
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
        raise InvalidCredentials()



@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp =  token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_acess_token = create_access_token(
            user_data= token_details['user']
        )
        return JSONResponse(
            {
                "access_token": new_acess_token
            }
        ) 

    raise ExpiredToken()

@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(
    user = Depends(get_current_user),
    _: bool = Depends(role_checker)):
    return user 


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blacklist(jti)

    return JSONResponse(
        content= {
            "message": "Logged Out Successfully"
        },
        status_code= status.HTTP_200_OK
    )

