from fastapi import FastAPI,status
from src.errors import *
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


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
)

app.add_exception_handler(
    UserAlreadyExists,
    Create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "Message":"User with same email already exists.",
            "Error Code": "user_exists"
        }
    )
)

app.add_exception_handler(
    InvalidToken,
    Create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "Message":"User provided a expired or revoked token",
            "Error Code": "user_token_expired"
        }
    )
)

app.add_exception_handler(
    RevokedToken,
    Create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "Message":"User provided a revoked token",
            "Error Code": "user_token_revoked"
        }
    )
)

app.add_exception_handler(
    AccessTokenRequired,
    Create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "Message":"Please provie a Access token"
        }
    )
)

app.add_exception_handler(
    RefreshTokenRequired,
    Create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "Message":"Please provie a Refresh token"
        }
    )
)

app.add_exception_handler(
    UserAlreadyExists,
    Create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "Message":"user already exists"
        }
    )
)

app.add_exception_handler(
    InsufficientPermission,
    Create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "Message":"user is not authorized for this action!"
        }
    )
)

app.add_exception_handler(
    InvalidEmail_Or_Password,
    Create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "Message":"Please provide a valid email and password."
        }
    )
)

app.add_exception_handler(
    LogoutFailed,
    Create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        initial_detail={
            "Message":"The system was not able log out the user sucessfully."
        }
    )
)

app.add_exception_handler(
    UnableToFetchResource,
    Create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "Message":"The system could not find the required entity in the database"
        }
    )
)

app.add_exception_handler(
    InternalServerError,
    Create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        initial_detail={
            "Message":"An internal server error has occured."
        }
    )
)


@app.exception_handler(500)
async def ISE(request,exc):
    return JSONResponse(
        content={"Message":"Oops! something went wrong", "ErrorCode":"500 ISR"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])
app.include_router(auth_router,prefix=f'/api/{version}/auth',tags=["Auth"])
app.include_router(review_router,prefix=f'/api/{version}/reviews',tags=["Reviews"])