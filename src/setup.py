import smtplib
import ssl
import sys

from celery import Celery
from celery.schedules import crontab
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.aggregator.database.connection import initialize_database
from src.config import Settings

settings = Settings()


def setup_fastapi() -> FastAPI:
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


def setup_celery() -> Celery:
    from src.aggregator.service_layer.backgruond_tasks import send_notifications

    celery_app = Celery('tasks', broker=settings.redis.broker_url + '0')
    app_task_send_notifications = celery_app.task(send_notifications)

    celery_app.conf.beat_schedule = {
        'run_every_24_hours': {
            'task': 'celery_app.app_task_send_notifications',
            'schedule': crontab(minute='0', hour='3'),
        }}

    return celery_app


async def get_session_maker() -> async_sessionmaker:
    engine = create_async_engine(settings.database.connection_string)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    await initialize_database(engine)

    return session_maker


async def setup_email_server() -> smtplib.SMTP_SSL:
    email_server = smtplib.SMTP_SSL(settings.stmp.server, settings.stmp.port, context=ssl.create_default_context())
    email_server.login(settings.stmp.name, settings.stmp.password)
    return email_server


def setup_logging():
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
