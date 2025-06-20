from fastapi import FastAPI,status
from src.errors import *
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.errors import register_Errors
from src.middleware import register_middleware

@asynccontextmanager
async def life_span(app :FastAPI):
    print("Server is starting...")
    await init_db()
    yield 
    print("Server has been stopped.")

version="v1"
app=FastAPI(
    title="Bookly",
    description="A REST API for book review web service.",
    version=version,
    terms_of_service=""
)
register_middleware(app)
register_Errors(app)

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])
app.include_router(auth_router,prefix=f'/api/{version}/auth',tags=["Auth"])
app.include_router(review_router,prefix=f'/api/{version}/reviews',tags=["Reviews"])