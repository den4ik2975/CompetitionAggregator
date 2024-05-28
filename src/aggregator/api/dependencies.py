from fastapi import Request
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchema


async def get_db_session(
        request: Request,
) -> async_session:
    """
    Fastapi dependency function for pretty data from middleware injecting

    Args:
        request: incoming request

    Returns: async_session from corresponding middleware

    """

    return request.state.db_session


async def get_auth(
        request: Request,
) -> UserSchema | bool:
    """
    Fastapi dependency function for pretty data from middleware injecting

    Args:
        request: incoming request

    Returns: async_session from corresponding middleware
    """

    return request.state.auth
