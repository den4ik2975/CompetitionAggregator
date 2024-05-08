from datetime import timedelta, datetime, timezone
from typing import List, Optional, Tuple, Coroutine

from fastapi import Depends
from loguru import logger

from src.aggregator.DTOs import OlympiadSchema, UserSchemaAdd, UserSchemaAuth, UserSchema, NotificationSchema
from src.aggregator.database import crud, get_session_maker
from src.aggregator.service_layer import utils
from src.project_logging import logging_wrapper
from src.setup import pwd_context, oauth2_scheme, settings


def session_service():
    return get_session_maker(settings.database.connection_string)


@logging_wrapper
async def get_olympiad(
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> OlympiadSchema:
    olympiad = await crud.get_olympiad_by_id(session_maker=await session_maker_getter,
                                             olympiad_id=olympiad_id)

    logger.info('Got olympiad')
    return olympiad.to_dto_model()


@logging_wrapper
async def get_olympiads(
        session_maker_getter: Coroutine = session_service(),
) -> List[OlympiadSchema]:
    olympiads = await crud.get_all_olympiads(session_maker=await session_maker_getter)
    dto_olympiads = [ol.to_dto_model() for ol in olympiads]

    logger.info('Got olympiads')
    return dto_olympiads


@logging_wrapper
async def get_user_by_id(
        user_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    user = await crud.get_user_by_id(session_maker=await session_maker_getter,
                                     user_id=user_id)

    logger.info('Got user')
    return user.to_dto_model()


@logging_wrapper
async def add_new_user(
        user: UserSchemaAdd,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    hashed_password = pwd_context.hash(user.password)
    user = await crud.add_user(session_maker=await session_maker_getter,
                               username=user.username,
                               mail=user.mail,
                               password=hashed_password)

    logger.info('Added new user')
    return user.to_dto_model()


@logging_wrapper
async def auth_user(
        user_login: UserSchemaAuth,
        session_maker_getter: Coroutine = session_service(),
) -> Optional[Tuple[UserSchema, str]]:
    logger.info('Try user auth')
    user = await crud.get_user_by_email(session_maker=await session_maker_getter,
                                        mail=user_login.login)
    if user is None:
        user = await crud.get_user_by_username(session_maker=await session_maker_getter,
                                               username=user_login.login)
    if user is None:
        return None

    if pwd_context.verify(user_login.password, user.hashed_password):
        access_token_expires = timedelta(minutes=settings.encryption.access_token_expire_minutes)
        access_token = await utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info('User auth success')
        return user.to_dto_model(), access_token

    logger.info('User auth failed')
    return None


@logging_wrapper
async def is_authenticated(
        session_maker_getter: Coroutine = session_service(),
        access_token: str = Depends(oauth2_scheme)
) -> bool:
    logger.info('Auth check')
    username = await utils.decode_access_token(access_token)
    user = await crud.get_user_by_username(session_maker=await session_maker_getter,
                                           username=username)

    if user is None:
        return False
    return True


@logging_wrapper
async def add_user_favorite(
        user_id: int,
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    user = await crud.update_user_favorites(session_maker=await session_maker_getter,
                                            user_id=user_id,
                                            olympiad_id=olympiad_id)

    logger.info('Added user favorite')
    return user.to_dto_model()


@logging_wrapper
async def delete_user_favorite(
        user_id: int,
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    user = await crud.delete_user_favorite(session_maker=await session_maker_getter,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user favorite')
    return user.to_dto_model()


@logging_wrapper
async def add_user_participate(
        user_id: int,
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    user = await crud.update_user_participate(session_maker=await session_maker_getter,
                                              user_id=user_id,
                                              olympiad_id=olympiad_id)

    logger.info('Added user participation')
    return user.to_dto_model()


@logging_wrapper
async def delete_user_participate(
        user_id: int,
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> UserSchema:
    user = await crud.delete_user_favorite(session_maker=await session_maker_getter,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user participation')
    return user.to_dto_model()


@logging_wrapper
async def add_notification(
        user_id: int,
        olympiad_id: int,
        session_maker_getter: Coroutine = session_service(),
) -> NotificationSchema:
    user = await crud.get_user_by_id(session_maker=await session_maker_getter,
                                     user_id=user_id)
    olympiad = await crud.get_olympiad_by_id(session_maker=await session_maker_getter,
                                             olympiad_id=olympiad_id)

    date_now: datetime = datetime.now(tz=timezone.utc)
    for date in olympiad.dates:
        if
    nearest_date: datetime = min(olympiad.dates)
    notification_date = nearest_date - timedelta(days=user.n)

    notification = await crud.add_notification(session_maker=await session_maker_getter,
                                               user_id=user_id,
                                               olympiad_id=olympiad_id,
                                               date=notification_date)

    return notification.to_dto_model()

