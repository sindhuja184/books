from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config
import uuid
import logging


password_context = CryptContext(
    schemes= ['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)

def create_access_token(
        user_data: dict, 
        expiry: timedelta = None,
        refresh: bool = False
    ):
    
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + expiry if  expiry is not None else timedelta(seconds= ACCESS_TOKEN_EXPIRY)
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        algorithm = Config.JWT_ALGORITHM,
        key= Config.JWT_SECRET
    )

    return token

def decode_token(token : str) -> dict:
    try:
        token_data = jwt.decode(
            jwt = token, 
            key = Config.JWT_SECRET,
            algorithms= [Config.JWT_ALGORITHM]

        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None