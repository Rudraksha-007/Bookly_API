from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
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