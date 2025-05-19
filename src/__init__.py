from fastapi import FastAPI
from src.books.routes import router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from src.recommender.routes import rec_router
from fastapi import status
from fastapi.responses import JSONResponse
from .middleware import register_middleware 

from .errors import register_all_errors
version = 'v1'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The server is starting..")
    from src.db.models import Book
    
    await init_db()
    yield
    print("The server has been stopped")

app = FastAPI(
    title= "Bookly",
    description = 'A REST API for a book review web service',
    version= version
)

register_all_errors(app=app)
register_middleware(app=app)

app.include_router(router=router, prefix=f'/api/{version}/books')
app.include_router(router = auth_router, prefix = f'/api/{version}/auth')
app.include_router(review_router, prefix= f'/api/{version}/reviews')
app.include_router(tags_router, prefix= f'/api/{version}/tags')
app.include_router(rec_router, prefix= f'/api/{version}/recommend')