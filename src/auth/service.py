from .models import User
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_password_hash, verify_password
class UserService:
    async def get_user_by_email(self, email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)

        user_row = result.first()
        user = user_row[0] if user_row else None
        return user

    
    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False 
    
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):

        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )
        
        user_exist = await self.user_exists(new_user.email, session)

        if not user_exist:
            new_user.password_hash = generate_password_hash(user_data_dict['password'])

            session.add(new_user)

            await session.commit()

            return new_user
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
    

