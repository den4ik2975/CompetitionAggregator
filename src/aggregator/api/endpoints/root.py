from typing import Any

from fastapi import APIRouter

from src.aggregator.DTOs import OlympiadSchema
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads(
        response_model=list[OlympiadSchema],
) -> Any:
    olympiads = await services.get_olympiads()

    return olympiads
