from fastapi import FastAPI
from src.books.routes import router

from contextlib import asynccontextmanager
from src.db.main import init_db

version = 'v1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The server is starting..")
    await init_db()
    yield
    print("The server has been stopped")

app = FastAPI(
    title= "Bookly",
    description = 'A REST API for a book review and web service',
    version= version,
    lifespan=lifespan
)

app.include_router(router=router, prefix=f'/api/{version}/books')
