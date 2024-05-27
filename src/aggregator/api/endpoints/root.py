from typing import List, Annotated

from fastapi import APIRouter, Depends
from loguru import logger

from src.aggregator.DTOs import OlympiadSchemaView
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads() -> List[OlympiadSchemaView]:
    logger.info('Request for olympiad cards')

    olympiads = await services.get_olympiads()

    return olympiads
