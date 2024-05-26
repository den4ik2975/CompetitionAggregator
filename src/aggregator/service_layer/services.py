from datetime import timedelta, datetime, timezone
from typing import List, Optional, Tuple

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.DTOs import OlympiadSchema, UserSchemaAdd, UserSchemaAuth, UserSchema, OlympiadSchemaView
from src.aggregator.database import crud
from src.aggregator.service_layer import utils
from src.aggregator.service_layer.utils import add_session_maker, logging_wrapper
from src.setup import pwd_context, oauth2_scheme, settings


@logging_wrapper
@add_session_maker
async def get_olympiad(
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> OlympiadSchema | None:
    olympiad = await crud.get_olympiad_by_id(session_maker=session_maker,
                                             olympiad_id=olympiad_id)

    logger.info('Got olympiad')
    if olympiad is None:
        return None
    return olympiad.to_dto_model()


@logging_wrapper
@add_session_maker
async def get_olympiads(
        auth: bool,
        session_maker: async_sessionmaker,
) -> List[OlympiadSchemaView]:
    olympiads = await crud.get_all_olympiads(session_maker=session_maker)

    card_olympiads = []
    for olympiad in olympiads:
        olympiad = olympiad.to_dto_model()

        card_olympiad = OlympiadSchemaView(
            id=olympiad.id,
            title=olympiad.title,
            description=olympiad.description,
            date=utils.get_nearest_date(olympiad),
            classes=utils.humanize_classes(olympiad),
            subjects=utils.optimize_subjects(olympiad)
        )

        card_olympiads.append(card_olympiad)

    logger.info('Got olympiad card')
    return card_olympiads


@logging_wrapper
@add_session_maker
async def get_user_by_id(
        user_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    user = await crud.get_user_by_id(session_maker=session_maker,
                                     user_id=user_id)

    logger.info('Got user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def add_new_user(
        user: UserSchemaAdd,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    hashed_password = pwd_context.hash(user.password)
    user = await crud.add_user(session_maker=session_maker,
                               username=user.username,
                               mail=user.mail,
                               password=hashed_password)

    logger.info('Added new user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def auth_user(
        user_login: UserSchemaAuth,
        session_maker: async_sessionmaker,
) -> Optional[Tuple[UserSchema, str]]:
    logger.info('Try user auth')
    user = await crud.get_user_by_email(session_maker=session_maker,
                                        mail=user_login.login)
    if user is None:
        user = await crud.get_user_by_username(session_maker=session_maker,
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
@add_session_maker
async def is_authenticated(
        session_maker: async_sessionmaker,
        access_token: str = Depends(oauth2_scheme)
) -> bool:
    logger.info('Auth check')

    username = await utils.decode_access_token(access_token)
    user = await crud.get_user_by_username(session_maker=session_maker,
                                           username=username)

    if user is None:
        return False
    return True


@logging_wrapper
@add_session_maker
async def add_user_favorite(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    user = await crud.update_user_favorites(session_maker=session_maker,
                                            user_id=user_id,
                                            olympiad_id=olympiad_id)

    logger.info('Added user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def delete_user_favorite(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    user = await crud.delete_user_favorite(session_maker=session_maker,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def add_user_participate(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    user = await crud.update_user_participate(session_maker=session_maker,
                                              user_id=user_id,
                                              olympiad_id=olympiad_id)

    logger.info('Added user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def delete_user_participate(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | None:
    user = await crud.delete_user_favorite(session_maker=session_maker,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def add_notifications(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | bool:
    user = await crud.get_user_by_id(session_maker=session_maker,
                                     user_id=user_id)
    olympiad = await crud.get_olympiad_by_id(session_maker=session_maker,
                                             olympiad_id=olympiad_id)

    if user is None or olympiad is None:
        return False

    date_now: datetime = datetime.now(tz=timezone.utc)
    for olympiad_date in olympiad.dates:
        if olympiad_date > (date_now + timedelta(days=user.n)):
            await crud.add_notification(session_maker=session_maker,
                                        user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        date=olympiad_date)

    return user.to_dto_model()


@logging_wrapper
@add_session_maker
async def delete_notifications(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker,
) -> UserSchema | bool:
    result = await crud.delete_notifications_by_user_and_olympiad_id(session_maker=session_maker,
                                                                     user_id=user_id,
                                                                     olympiad_id=olympiad_id)

    if result is None:
        return False
    return True


@logging_wrapper
@add_session_maker
async def get_notifications(
        user_id: int,
        olympiad_id: int,
        session_maker: async_sessionmaker
) -> bool:
    notifications = await crud.get_notifications_by_user_and_olympiad_id(session_maker=session_maker,
                                                                         user_id=user_id,
                                                                         olympiad_id=olympiad_id)

    if notifications:
        return True
    return False
