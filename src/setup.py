from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.config import Settings


def get_fastapi_app() -> FastAPI:
    from src.aggregator.api.router import all_routers

    app_fastapi = FastAPI()

    origins = settings.fastapi.origins

    # noinspection PyTypeChecker
    app_fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in all_routers:
        app_fastapi.include_router(router)

    return app_fastapi


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = Settings()

