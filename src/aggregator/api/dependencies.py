from fastapi import Request
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchema


async def get_db_session(
        request: Request,
) -> async_session:
    return request.state.db_session


async def get_auth(
        request: Request,
) -> UserSchema | bool:
    return request.state.auth
