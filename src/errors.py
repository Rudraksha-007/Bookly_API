from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI,status
class BooklyExceptions(Exception):
    """This is the default base class for all the bookly API exceptions and errors"""

    pass


class InvalidToken(BooklyExceptions):
    """User has provided a expired or invalid token"""

    pass


class RevokedToken(BooklyExceptions):
    """User has provided a Revoked token"""

    pass


class AccessTokenRequired(BooklyExceptions):
    """User has provided a Refresh token when a access token was required"""

    pass


class RefreshTokenRequired(BooklyExceptions):
    """User has provided a access token when a refresh token was required"""

    pass


class UserAlreadyExists(BooklyExceptions):
    """The Email provided already has a user registerd in the database"""

    pass


class InsufficientPermission(BooklyExceptions):
    """User does'nt possess valid credentials"""

    pass


class InvalidEmail_Or_Password(BooklyExceptions):
    """User has provided invalid credentials"""

    pass


class LogoutFailed(BooklyExceptions):
    """The system was not able log out the user sucessfully."""

    pass


class UnableToFetchResource(BooklyExceptions):
    """The system could not find the required entity in the database"""

    pass


class InternalServerError(BooklyExceptions):
    """An internal server error has occured."""

    pass


def Create_exception_handler(status_code:int,initial_detail:Any)->Callable[[Request,Exception],JSONResponse]:#type:ignore

    async def exception_handler(request:Request,exc:BooklyExceptions):

        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    
    return exception_handler # type: ignore


def register_Errors(app:FastAPI):
        
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


    app.exception_handler(500)
    async def ISE(request,exc):
        return JSONResponse(
            content={"Message":"Oops! something went wrong", "ErrorCode":"500 ISR"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    