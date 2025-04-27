from fastapi import FastAPI
from .books.routes import router


version = 'v1'


app = FastAPI(
    title= "Bookly",
    description = 'A REST API for a book review and web service',
    version= version
)

app.include_router(router=router, prefix = f'/api/{version}/books')

