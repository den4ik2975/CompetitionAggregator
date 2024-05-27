from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.aggregator.service_layer.services import is_authenticated
from src.setup import get_session_maker


class DatabaseSessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        session_maker = await get_session_maker()

        async with session_maker() as session:
            request.state.db_session = session

            response = await call_next(request)
            return response


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_auth = await is_authenticated(request, request.state.db_session)

        request.state.auth = is_auth

        response = await call_next(request)
        return response
