from typing import Annotated, Tuple

from fastapi import APIRouter, Depends, Body, Path

from src.aggregator.DTOs import OlympiadSchema, UserSchema
from src.aggregator.service_layer import services

router_olympiad = APIRouter(
    prefix="/olympiad",
    tags=["Olympiad"],
)


@router_olympiad.get("/{olympiad_id}")
async def get_olympiad(
        olympiad_id: Annotated[int, Path()],
        user_id: Annotated[int, Body()],
        is_auth: Annotated[bool, Depends(services.is_authenticated)],
        response_model=Tuple[OlympiadSchema, UserSchema]
):
    user = None
    if is_auth:
        user = await services.get_user_by_id(user_id=user_id)
    olympiad = services.get_olympiad(olympiad_id=olympiad_id)

    return olympiad, user
