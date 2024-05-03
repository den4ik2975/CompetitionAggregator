from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.service_layer import services
from src.aggregator.api import OlympiadSchema, session_service


router_olympiad = APIRouter(
    prefix="/olympiad",
    tags=["Olympiad"],
)


@router_olympiad.get("/{olympiad_id}")
async def get_olympiad(
        olympiad_id: Annotated[int, Path()],
        user_id: Annotated[int, Body()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
):
    ...

