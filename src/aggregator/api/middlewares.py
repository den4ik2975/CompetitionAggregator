from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.aggregator.service_layer.services import is_authenticated
from src.setup import get_session_maker


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware class for injecting a db session

    Methods:
        dispatch(self, request: Request, call_next): main middleware class
    """

    async def dispatch(self, request: Request, call_next):
        """
        Gets session maker and with using of context manager injects it into request
        After sending response session close automatically (thanks with)

        Args:
            request: incoming request object
            call_next:

        Returns: request
        """

        session_maker = await get_session_maker()

        async with session_maker() as session:
            request.state.db_session = session

            response = await call_next(request)
            return response


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware class for checking user's authentication

    Methods:
        dispatch(self, request: Request, call_next): main middleware class
    """

    async def dispatch(self, request: Request, call_next):
        """
        Checks request cookie for access token availability
        If there is a token, decode it and try to find corresponding user.
        If succeed return UserSchema.
        In other cases returns False

        Args:
            request: incoming request object
            call_next:

        Returns: response

        """
        is_auth = await is_authenticated(request, request.state.db_session)

        request.state.auth = is_auth

        response = await call_next(request)
        return response
