from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession


async_engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    future=True  # Ensure the future flag is set for async support
)

async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind = async_engine, 
        class_ = AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session