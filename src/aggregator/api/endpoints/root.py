from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.DTOs import OlympiadSchema
from src.aggregator.api import session_service
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads(
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
) -> List[OlympiadSchema]:
    olympiads = await services.get_olympiads(session_maker)

    return olympiads
