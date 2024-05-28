from typing import Annotated, List

from fastapi import APIRouter, Body, Path, Depends, status, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchema, OlympiadSchemaCard
from src.aggregator.api.dependencies import get_auth, get_db_session
from src.aggregator.service_layer import services

router_user = APIRouter(
    prefix='/user',
)


@router_user.get('/{user_id}/favorites', tags=['Favorites'])
async def get_favorite(
        user_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> List[OlympiadSchemaCard]:
    """
    Get a list of favorite olympiads for a user.

    Args:
        user_id (int): ID of the user.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        List[OlympiadSchemaCard]: List of favorite olympiads for the user.
    """
    logger.info('Request for user favorites')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response_data = await services.get_user_choices(user_id=user_id,
                                                    auth=auth,
                                                    key='favorites',
                                                    db_session=db_session)

    return response_data


@router_user.post('/{user_id}/favorites', tags=['Favorites'])
async def add_favorite(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    """
    Add an olympiad to the user's favorites.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to add to favorites.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data.
    """
    logger.info('Request to add favorites')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
    """
    Remove an olympiad from the user's favorites.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to remove from favorites.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data.
    """
    logger.info('Request to delete favorites')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await services.delete_user_favorite(user_id=user_id,
                                               olympiad_id=olympiad_id,
                                               db_session=db_session)
    return user


@router_user.get('/{user_id}/participates', tags=['Participates'])
async def add_participate(
        user_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> List[OlympiadSchemaCard]:
    """
    Get a list of olympiads that the user is participating in.

    Args:
        user_id (int): ID of the user.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        List[OlympiadSchemaCard]: List of olympiads the user is participating in.
    """
    logger.info('Request to get participations')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response_data = await services.get_user_choices(user_id=user_id,
                                                    auth=auth,
                                                    key='participates',
                                                    db_session=db_session, )

    return response_data


@router_user.post('/{user_id}/participates', tags=['Participates'])
async def add_participate(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    """
    Add an olympiad to the user's list of participated olympiads.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to add to participated list.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data.
    """
    logger.info('Request to add participates')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
    """
    Remove an olympiad from the user's list of participated olympiads.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to remove from participated list.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data.
    """
    logger.info('Request to delete participates')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await services.delete_user_participate(user_id=user_id,
                                                  olympiad_id=olympiad_id,
                                                  db_session=db_session)
    return user


@router_user.get('/{user_id}/notifications', tags=['Notifications'])
async def get_notifications(
        user_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> List[OlympiadSchemaCard]:
    """
    Retrieve a list of olympiads for which the user has set notifications.

    Args:
        user_id (int): ID of the user.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        List[OlympiadSchemaCard]: List of olympiads for which the user has set notifications.
    """
    logger.info('Request to get notifications')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response_data = await services.get_user_choices(user_id=user_id,
                                                    auth=auth,
                                                    key='notifications',
                                                    db_session=db_session, )

    return response_data


@router_user.post('/{user_id}/notifications', tags=['Notifications'])
async def add_notifications(
        user_id: Annotated[int, Path()],
        olympiad_id: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    """
    Add an olympiad to the user's notifications list.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to add to the notifications list.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data after adding the olympiad to the notifications list.
    """
    logger.info('Request to add notifications')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
    """
    Remove an olympiad from the user's notifications list.

    Args:
        user_id (int): ID of the user.
        olympiad_id (int): ID of the olympiad to remove from the notifications list.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
    """
    logger.info('Request to delete notifications')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await services.delete_notifications(user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        db_session=db_session)


@router_user.post('/{user_id}/change_n', tags=['Changer'])
async def change_user_n(
        user_id: Annotated[int, Path()],
        n: Annotated[int, Body()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    """
    Change the value of 'n' for the user.

    Args:
        user_id (int): ID of the user.
        n (int): New value of 'n' for the user.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: Updated user data with the new value of 'n'.
    """
    logger.info("Request to change user's n")

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await services.change_n(user_id=user_id,
                                   new_n=n,
                                   db_session=db_session)

    return user


@router_user.get('/{user_id}', tags=['User'])
async def go_to_user(
        user_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    """
    Retrieve user data by user ID.

    Args:
        user_id (int): ID of the user.
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.

    Returns:
        401 code if user is unauthorized
        UserSchema: User data for the specified user ID.
    """
    logger.info('Request for user data')

    if auth is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await services.get_user_by_id(user_id=user_id,
                                         db_session=db_session)
    return user
