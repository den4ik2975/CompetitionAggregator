from typing import Annotated, List

from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.service_layer import services
from src.aggregator.api import session_service
from src.aggregator.DTOs import UserSchemaAdd, UserSchema, UserSchemaAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router_auth.post("/register")
async def register_user(
        user: Annotated[UserSchemaAdd, Body()],
        session_maker: async_sessionmaker = Depends(session_service)
) -> UserSchema:
    user = await services.add_new_user(session_maker=session_maker, user=user)
    return user


@router_auth.post("")
async def login_user(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        session_maker: async_sessionmaker = Depends(session_service),
) -> UserSchema:
    user_login = UserSchemaAuth(login=login_data.username, password=login_data.password)
    user, access_token = await services.auth_user(session_maker=session_maker, user_login=user_login)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return user











