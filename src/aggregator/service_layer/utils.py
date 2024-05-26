import asyncio
import smtplib
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

import stackprinter
from fastapi import Depends
from jose import jwt
from loguru import logger

from src.aggregator.DTOs.olympiad import OlympiadSchema
from src.aggregator.database import crud
from src.setup import oauth2_scheme, settings, get_session_maker


def add_session_maker(func):
    async def wrapper(*args, **kwargs):
        session_maker = await get_session_maker()
        return await func(session_maker=session_maker, *args, **kwargs)

    return wrapper


def logging_wrapper(func):
    async def wrapper(*args, **kwargs):
        with logger.contextualize(**kwargs), logger.catch():
            return await func(*args, **kwargs)

    return wrapper


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.encryption.secret_key, algorithm=settings.encryption.algorithm)

    logger.info('Generated access token')
    return encoded_jwt


async def decode_access_token(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, settings.encryption.secret_key, algorithms=[settings.encryption.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
    except (jwt.JWTError, AttributeError):
        return None

    logger.info('Decoded access token')
    return username


@logging_wrapper
async def send_email(email_server: smtplib.SMTP_SSL, receiver_email: str, body: str):
    email_server.sendmail(settings.stmp.name, receiver_email, body)

    logger.info(f'Sent email to {receiver_email}')


def async_logging_binder():
    asyncio.run(logger.bind(async_logging_binder=database_sink).enqueue(database_sink).start())


async def database_sink(message):
    session_maker = await get_session_maker()
    record = message.record

    user_id = record["extra"]["user_id"]
    level = record["level"].name
    text = record["message"]
    if record["exception"]:
        text += "\n" + stackprinter.format(record["exception"])

    if level in ("ERROR", "CRITICAL", "EXCEPTION"):
        log_type = LogTypes.exceptions
    else:
        log_type = LogTypes.user if user_id else LogTypes.system

    await crud.add_log(
        session_maker=session_maker,
        user_id=user_id,
        log_type=log_type.value,
        date=datetime.now(),
        text=text)


def placeholder(*args, **kwargs):
    pass


async def get_nearest_date(olympiad: OlympiadSchema) -> datetime:
    now = datetime.now(tz=timezone.utc)

    for dates in olympiad.dates.values():
        if now < dates[0]:
            return dates[0]


async def humanize_classes(olympiad: OlympiadSchema) -> str:
    classes = ''
    if len(olympiad.classes) == 1:
        classes = f'{olympiad.classes[1]} класс'
    else:
        classes = f'{min(olympiad.classes)} - {max(olympiad.classes)} классы'

    return classes


async def optimize_subjects(olympiad: OlympiadSchema) -> str:
    language_flag = 0
    subjects = ''

    for subject in olympiad.subjects:
        if 'язык' in subject.lower():
            language_flag = 1
        else:
            subjects += '{' + f'{subject}' + '}, '

    if language_flag is True:
        subjects += '{Языковедение}'
    else:
        subjects = subjects[:-2]

    return subjects


class LogTypes(Enum):
    system = 0
    exceptions = 1
    user = 2
