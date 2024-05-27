from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchemaAdd, UserSchema, UserSchemaAuth
from src.aggregator.api.dependencies import get_db_session, get_auth
from src.aggregator.service_layer import services

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router_auth.post("/register")
async def register_user(
        user: Annotated[UserSchemaAdd, Body()],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> UserSchema:
    logger.info(f"Request to register user: {user.username}")

    user = await services.add_new_user(user=user,
                                       db_session=db_session)
    return user


@router_auth.post("")
async def login_user(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
        response: Response,
) -> UserSchema:
    logger.info(f"Request to login user: {login_data.username}")

    user_login = UserSchemaAuth(login=login_data.username, password=login_data.password)
    user, access_token = await services.auth_user(user_login=user_login,
                                                  db_session=db_session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return user
