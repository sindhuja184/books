from fastapi import FastAPI
from src.books.routes import router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

version = 'v1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The server is starting..")
    from src.books.models import Book
    
    await init_db()
    yield
    print("The server has been stopped")

app = FastAPI(
    title= "Bookly",
    description = 'A REST API for a book review and web service',
    version= version
)

app.include_router(router=router, prefix=f'/api/{version}/books')
app.include_router(router = auth_router, prefix = f'/api/{version}/auth')
