import asyncio
import smtplib
import ssl
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from rocketry import Rocketry
from rocketry.conds import weekly
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.middleware import Middleware

from src.aggregator.database.connection import initialize_database
from src.config import Settings

settings = Settings()


def setup_fastapi() -> FastAPI:
    """
    Setups FastAPI app providing docs, origins, middlewares and routers

    Returns: FastAPI app

    """
    from src.aggregator.api.router import all_routers
    from src.aggregator.api.middlewares import AuthenticationMiddleware, DatabaseSessionMiddleware

    tags_metadata = [
        {
            "name": "Auth",
            "description": "User register and login here",
        },
        {
            "name": "Olympiad",
            "description": "Method for getting olympiad information",
        },
        {
            "name": "Root",
            "description": "Root endpoint. Returns short description of olympiads",
        },
        {
            "name": "User",
            "description": "Get user info",
        },
        {
            "name": "Favorites",
            "description": "Actions with favorites",
        },
        {
            "name": "Participates",
            "description": "Actions with participates",
        },
        {
            "name": "Notifications",
            "description": "Actions with notifications",
        }
    ]

    origins = settings.fastapi.origins

    # noinspection PyTypeChecker
    app_fastapi = FastAPI(
        title="Competition Aggregator API",
        openapi_tags=tags_metadata,
        middleware=[
            Middleware(DatabaseSessionMiddleware),
            Middleware(AuthenticationMiddleware),
            Middleware(CORSMiddleware,
                       allow_origins=origins,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])
        ])

    for router in all_routers:
        app_fastapi.include_router(router)

    return app_fastapi


def setup_rocketry() -> None:
    """
    Setups Rocketry (task scheduler) for background tasks: send notifications and parse olympiads

    Returns: None

    """
    from src.aggregator.service_layer.backgruond_tasks import send_notifications, update_olympiads_info

    app_rocketry = Rocketry(execution="async")

    @app_rocketry.task("daily between 03:00 and 04:00")
    async def send_ntfs():
        await asyncio.sleep(0)

        await send_notifications()

    @app_rocketry.task(weekly.on("Monday"))
    async def upd_info():
        await asyncio.sleep(0)

        await update_olympiads_info()

    asyncio.run(app_rocketry.serve())


async def get_session_maker() -> async_sessionmaker:
    """
    Setups session maker getter for database

    Returns: async_sessionmaker

    """
    engine = create_async_engine(settings.database.connection_string)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    await initialize_database(engine)

    return session_maker


async def setup_email_server() -> smtplib.SMTP_SSL:
    """
    Setups email server for sending ntfs

    Returns: server
    """
    email_server = smtplib.SMTP_SSL(settings.stmp.server, settings.stmp.port, context=ssl.create_default_context())
    email_server.login(settings.stmp.name, settings.stmp.password)
    return email_server


def setup_logging():
    """
    Setups loguru

    Returns: None

    """
    from src.aggregator.service_layer.utils import database_sink

    logger.remove()
    logger.add(
        database_sink,
        enqueue=True,
        format="[{time:YYYY-MM-DD HH:mm:ss}] ({extra[user_id]:^12} | <b><level>{extra[name]:^18}</level></b>) → {message}\n{exception}",
        backtrace=True,
        diagnose=True,
        level=("INFO"),

    )
    logger.add(
        sys.stdout,
        format="[{time:YYYY-MM-DD HH:mm:ss}] ({extra[user_id]:^12} | <b><level>{extra[name]:^18}</level></b>) → {message}",
        backtrace=True,
        diagnose=True,
        colorize=True,
    )

    logger.configure(extra={"user_id": 0, "name": "System"})

    logger.level("TRACE", color="<cyan>")
    logger.level("DEBUG", color="<cyan>")
    logger.level("INFO", color="<blue>")
    logger.level("SUCCESS", color="<green>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<light-red>")
    logger.level("CRITICAL", color="<red>")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
