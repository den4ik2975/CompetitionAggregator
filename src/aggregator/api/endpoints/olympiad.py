from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.service_layer import services
from src.aggregator.api import session_service
from src.aggregator.DTOs import OlympiadSchema, UserSchema


router_olympiad = APIRouter(
    prefix="/olympiad",
    tags=["Olympiad"],
)


@router_olympiad.get("/{olympiad_id}")
async def get_olympiad(
        olympiad_id: Annotated[int, Path()],
        user_id: Annotated[int, Body()],
        is_auth: Annotated[bool, Depends(services.is_authenticated)],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
) -> (OlympiadSchema, UserSchema):
    user = None
    if is_auth:
        user = await services.get_user(user_id=user_id, session_maker=session_maker)
    olympiad = services.get_olympiad(olympiad_id=olympiad_id, session_maker=session_maker)

    return olympiad, user


