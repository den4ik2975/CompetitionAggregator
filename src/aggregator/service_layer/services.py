from datetime import timedelta, datetime, timezone
from typing import List, Optional, Tuple

from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchemaAdd, UserSchemaAuth, UserSchema, OlympiadSchemaView, \
    OlympiadSchemaOut
from src.aggregator.database import crud
from src.aggregator.service_layer import utils
from src.aggregator.service_layer.utils import logging_wrapper
from src.setup import pwd_context, settings


@logging_wrapper
async def get_olympiad(
        olympiad_id: int,
        auth: UserSchema | bool,
        db_session: async_session,
) -> OlympiadSchemaOut | None:
    olympiad = await crud.get_olympiad_by_id(session=db_session,
                                             olympiad_id=olympiad_id)

    logger.info('Got olympiad')
    print(olympiad.__dict__)
    is_favorite, is_notified, is_participant = False, False, False

    if olympiad is None:
        return None

    if auth is not False:
        if olympiad.id in auth.participates:
            is_participant = True
        if olympiad.id in auth.favorites:
            is_favorite = True
        if olympiad.id in auth.notifications:
            is_notified = True

    return OlympiadSchemaOut(
        id=olympiad.id,
        title=olympiad.title,
        level=olympiad.level,
        dates=olympiad.dates,
        description=olympiad.description,
        subjects=olympiad.subjects,
        classes=olympiad.classes,
        is_favorite=is_favorite,
        is_notified=is_notified,
        is_participant=is_participant
    )


@logging_wrapper
async def get_olympiads(
        auth: UserSchema | bool,
        db_session: async_session,
) -> List[OlympiadSchemaView]:
    olympiads = await crud.get_all_olympiads(session=db_session)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=olympiads,
                                                                  auth=auth)

    logger.info('Got olympiad card')
    return card_olympiads


@logging_wrapper
async def get_user_by_id(
        user_id: int,
        db_session: async_session,
) -> UserSchema | None:
    user = await crud.get_user_by_id(session=db_session,
                                     user_id=user_id)

    logger.info('Got user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_new_user(
        user: UserSchemaAdd,
        db_session: async_session,
) -> UserSchema | None:
    hashed_password = pwd_context.hash(user.password)
    user = await crud.add_user(session=db_session,
                               username=user.username,
                               mail=user.mail,
                               password=hashed_password)

    logger.info('Added new user')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def auth_user(
        user_login: UserSchemaAuth,
        db_session: async_session,
) -> Optional[Tuple[UserSchema | None, str | None]]:
    logger.info('Try user auth')
    user = await crud.get_user_by_email(session=db_session,
                                        mail=user_login.login)
    if user is None:
        user = await crud.get_user_by_username(session=db_session,
                                               username=user_login.login)
    if user is None:
        return None, None

    if pwd_context.verify(user_login.password, user.hashed_password):
        access_token_expires = timedelta(minutes=settings.encryption.access_token_expire_minutes)
        access_token = await utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info('User auth success')
        return user.to_dto_model(), access_token

    logger.info('User auth failed')
    return None, None


@logging_wrapper
async def is_authenticated(
        request: Request,
        db_session: async_session,
) -> UserSchema | bool:
    logger.info('Auth check')

    access_token = request.cookies.get('access_token')

    if not access_token:
        return False

    access_token = access_token.replace('Bearer ', '')

    username = await utils.decode_access_token(access_token)
    user = await crud.get_user_by_username(session=db_session, username=username)

    if user is None:
        logger.info('Auth check failed')
        return False

    return user.to_dto_model()


@logging_wrapper
async def add_user_favorite(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    user = await crud.update_user_favorites(session=db_session,
                                            user_id=user_id,
                                            olympiad_id=olympiad_id)

    logger.info('Added user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def delete_user_favorite(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    user = await crud.delete_user_favorite(session=db_session,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user favorite')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_user_participate(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    user = await crud.update_user_participate(session=db_session,
                                              user_id=user_id,
                                              olympiad_id=olympiad_id)

    logger.info('Added user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def delete_user_participate(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | None:
    user = await crud.delete_user_favorite(session=db_session,
                                           user_id=user_id,
                                           olympiad_id=olympiad_id)

    logger.info('Deleted user participation')
    if user is None:
        return None
    return user.to_dto_model()


@logging_wrapper
async def add_notifications(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | bool:
    user = await crud.get_user_by_id(session=db_session,
                                     user_id=user_id)
    olympiad = await crud.get_olympiad_by_id(session=db_session,
                                             olympiad_id=olympiad_id)

    if user is None or olympiad is None:
        return False

    date_now: datetime = datetime.now(tz=timezone.utc)
    for olympiad_date in olympiad.dates:
        if olympiad_date > (date_now + timedelta(days=user.n)):
            await crud.add_notification(session=db_session,
                                        user_id=user_id,
                                        olympiad_id=olympiad_id,
                                        date=olympiad_date)

    return user.to_dto_model()


@logging_wrapper
async def delete_notifications(
        user_id: int,
        olympiad_id: int,
        db_session: async_session,
) -> UserSchema | bool:
    result = await crud.delete_notifications_by_user_and_olympiad_id(session=db_session,
                                                                     user_id=user_id,
                                                                     olympiad_id=olympiad_id)

    if result is None:
        return False
    return True


@logging_wrapper
async def get_notifications(
        user_id: int,
        olympiad_id: int,
        db_session: async_session
) -> bool:
    notifications = await crud.get_notifications_by_user_and_olympiad_id(session=db_session,
                                                                         user_id=user_id,
                                                                         olympiad_id=olympiad_id)

    if notifications:
        return True
    return False


@logging_wrapper
async def search_olympiads(
        search_string: str,
        auth: UserSchema | bool,
        db_session: async_session,
) -> List[OlympiadSchemaView]:
    logger.info(f'Started searching olympiads with query: {search_string}')

    results = await crud.search_for_olympiads(session=db_session,
                                              search_string=search_string)

    card_olympiads = await utils.convert_olympiads_to_view_format(olympiads=results,
                                                                  auth=auth)

    return card_olympiads
