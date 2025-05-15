from src.db.models import User
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_password_hash, verify_password
from src.errors import UserAlreadyExists

class UserService:
    async def get_user_by_email(self, email:str, session: AsyncSession):
        statement = select(User).options(selectinload(User.books)).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    
    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return user is not None
    
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):

        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )
        
        user_exist = await self.user_exists(new_user.email, session)

        if not user_exist:
            new_user.password_hash = generate_password_hash(user_data_dict['password'])

            new_user.role = "user"
            session.add(new_user)

            await session.commit()
            await session.refresh(new_user)
            return new_user
        
        else:
            raise UserAlreadyExists()
    

