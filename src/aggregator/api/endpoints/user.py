from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.DTOs import UserSchema
from src.aggregator.api import session_service
from src.aggregator.service_layer import services

router_user = APIRouter(
    prefix='/user',
    tags=['User'],
)


@router_user.post('/{user_id}/favorites')
async def add_fav(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)],
) -> UserSchema:
    user = await services.add_user_favorite(session_maker=session_maker,
                                            user_id=user_id,
                                            olympiad_id=olympiad_id)
    return user


@router_user.delete('/{user_id}/favorites/{olympiad_id}')
async def delete_fav(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
) -> UserSchema:
    user = await services.delete_user_favorite(session_maker=session_maker,
                                               user_id=user_id,
                                               olympiad_id=olympiad_id)
    return user


@router_user.post('/{user_id}/participates')
async def add_prt(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)],
) -> UserSchema:
    user = await services.add_user_participate(session_maker=session_maker,
                                               user_id=user_id,
                                               olympiad_id=olympiad_id)
    return user


@router_user.delete('/{user_id}/favorites/{olympiad_id}')
async def delete_prt(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
) -> UserSchema:
    user = await services.delete_user_participate(session_maker=session_maker,
                                                  user_id=user_id,
                                                  olympiad_id=olympiad_id)
    return user


@router_user.get('/{user_id}')
async def go_to_user(
        user_id: Annotated[int, Body()],
        session_maker: Annotated[async_sessionmaker, Depends(session_service)]
) -> UserSchema:
    user = await services.get_user_by_id(session_maker=session_maker, user_id=user_id)
    return user
