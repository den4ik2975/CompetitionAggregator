from datetime import timedelta
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.api import session_service
from src.aggregator.database import crud
from src.project_logging import logging_wrapper
from src.aggregator.DTOs import OlympiadSchema, UserSchemaAdd, UserSchemaAuth, UserSchema
from src.aggregator.setup import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from src.aggregator.service_layer import utils


@logging_wrapper
async def get_olympiad(olympiad_id: int, session_maker: async_sessionmaker):
    olympiad = await crud.get_olympiad_by_id(session_maker=session_maker, olympiad_id=olympiad_id)
    return olympiad


@logging_wrapper
async def get_user(user_id: int, session_maker: async_sessionmaker) -> UserSchema:
    user = await crud.get_user_by_id(session_maker=session_maker, user_id=user_id)
    return user.to_dto_model()


@logging_wrapper
async def get_olympiads(
        session_maker: async_sessionmaker
) -> List[OlympiadSchema]:
    olympiads = await crud.get_all_olympiads(session_maker=session_maker)
    olympiads_to_pyd = [olympiad.to_dto_model() for olympiad in olympiads]

    return olympiads_to_pyd


@logging_wrapper
async def add_new_user(
        session_maker: async_sessionmaker,
        user: UserSchemaAdd
) -> UserSchema:
    hashed_password = pwd_context.hash(user.password)
    user = await crud.add_user(session_maker=session_maker, username=user.username, mail=user.mail,
                               password=hashed_password)
    return user.to_dto_model()


@logging_wrapper
async def auth_user(
        session_maker: async_sessionmaker,
        user_login: UserSchemaAuth
) -> Optional[(UserSchema, str)]:
    user = await crud.get_user_by_email(session_maker=session_maker, mail=user_login.login)
    if user is None:
        user = await crud.get_user_by_username(session_maker=session_maker, username=user_login.login)
    if user is None:
        return None

    if pwd_context.verify(user_login.password, user.hashed_password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return user, access_token

    return None


@logging_wrapper
async def is_authenticated(
        session_maker: async_sessionmaker = Depends(session_service),
        access_token: str = Depends(oauth2_scheme)
) -> bool:
    username = await utils.decode_access_token(access_token)
    user = await crud.get_user_by_username(session_maker=session_maker, username=username)

    if user is None:
        return False
    return True
