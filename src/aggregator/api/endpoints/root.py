from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.DTOs import OlympiadSchema
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads() -> List[OlympiadSchema]:
    olympiads = await services.get_olympiads()

    return olympiads
