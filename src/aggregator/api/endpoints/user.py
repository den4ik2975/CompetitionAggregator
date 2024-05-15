from typing import Annotated

from fastapi import APIRouter, Body, Path

from src.aggregator.DTOs import UserSchema
from src.aggregator.service_layer import services

router_user = APIRouter(
    prefix='/user',
    tags=['User'],
)


@router_user.post('/{user_id}/favorites')
async def add_fav(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
) -> UserSchema:
    user = await services.add_user_favorite(user_id=user_id,
                                            olympiad_id=olympiad_id)
    return user


@router_user.delete('/{user_id}/favorites/{olympiad_id}')
async def delete_fav(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
) -> UserSchema:
    user = await services.delete_user_favorite(user_id=user_id,
                                               olympiad_id=olympiad_id)
    return user


@router_user.post('/{user_id}/participates')
async def add_prt(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
) -> UserSchema:
    user = await services.add_user_participate(user_id=user_id,
                                               olympiad_id=olympiad_id)
    return user


@router_user.delete('/{user_id}/participates/{olympiad_id}')
async def delete_prt(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
) -> UserSchema:
    user = await services.delete_user_participate(user_id=user_id,
                                                  olympiad_id=olympiad_id)
    return user


@router_user.get('/{user_id}/notifications')
async def add_ntf(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
):
    has_notification = await services.get_notifications(user_id=user_id,
                                                        olympiad_id=olympiad_id)
    return {'has_notification': has_notification}


@router_user.post('/{user_id}/notifications')
async def add_ntf(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
):
    await services.add_notifications(user_id=user_id,
                                     olympiad_id=olympiad_id)


@router_user.delete('/{user_id}/notifications/{olympiad_id}')
async def delete_ntf(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
):
    await services.delete_notifications(user_id=user_id,
                                        olympiad_id=olympiad_id)


@router_user.get('/{user_id}')
async def go_to_user(
        user_id: Annotated[int, Body()],
) -> UserSchema:
    user = await services.get_user_by_id(user_id=user_id)
    return user
