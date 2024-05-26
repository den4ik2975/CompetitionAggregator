from typing import Annotated, Dict

from fastapi import APIRouter, Depends, Body, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.aggregator.DTOs import UserSchemaAdd, UserSchema, UserSchemaAuth
from src.aggregator.service_layer import services

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router_auth.post("/register")
async def register_user(
        user: Annotated[UserSchemaAdd, Body()],
) -> Dict[str, UserSchema]:
    user = await services.add_new_user(user=user)
    return {"User": user}


@router_auth.post("")
async def login_user(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
) -> Dict[str, UserSchema]:
    user_login = UserSchemaAuth(login=login_data.username, password=login_data.password)
    user, access_token = await services.auth_user(user_login=user_login)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"user": user}
