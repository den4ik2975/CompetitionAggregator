from typing import Annotated, Dict

from fastapi import APIRouter, Body, Path, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchema
from src.aggregator.api.dependencies import get_auth, get_db_session
from src.aggregator.service_layer import services

router_user = APIRouter(
    prefix='/user',
)


@router_user.post('/{user_id}/favorites', tags=['Favorites'])
async def add_favorite(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request to add favorites')

    user = await services.add_user_favorite(user_id=user_id,
                                            olympiad_id=olympiad_id,
                                            db_session=db_session)
    return user


@router_user.delete('/{user_id}/favorites/{olympiad_id}', tags=['Favorites'])
async def delete_favorite(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request to delete favorites')

    user = await services.delete_user_favorite(user_id=user_id,
                                               olympiad_id=olympiad_id,
                                               db_session=db_session)
    return user


@router_user.post('/{user_id}/participates', tags=['Participates'])
async def add_participate(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request to add participates')

    user = await services.add_user_participate(user_id=user_id,
                                               olympiad_id=olympiad_id,
                                               db_session=db_session)
    return user


@router_user.delete('/{user_id}/participates/{olympiad_id}', tags=['Participates'])
async def delete_participate(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request to delete participates')

    user = await services.delete_user_participate(user_id=user_id,
                                                  olympiad_id=olympiad_id,
                                                  db_session=db_session)
    return user


@router_user.get('/{user_id}/notifications', tags=['Notifications'])
async def get_notifications(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> Dict[str, bool]:
    logger.info('Request to get notifications')

    has_notification = await services.get_notifications(user_id=user_id,
                                                        olympiad_id=olympiad_id,
                                                        db_session=db_session)
    return {'has_notification': has_notification}


@router_user.post('/{user_id}/notifications', tags=['Notifications'])
async def add_notifications(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request to add notifications')

    user = await services.add_notifications(user_id=user_id,
                                            olympiad_id=olympiad_id,
                                            db_session=db_session)

    return user


@router_user.delete('/{user_id}/notifications/{olympiad_id}', tags=['Notifications'])
async def delete_notifications(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
):
    logger.info('Request to delete notifications')

    await services.delete_notifications(user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        db_session=db_session)


@router_user.get('/{user_id}', tags=['User'])
async def go_to_user(
        user_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info('Request for user data')

    user = await services.get_user_by_id(user_id=user_id,
                                         db_session=db_session)
    return user
