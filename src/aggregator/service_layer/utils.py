import smtplib
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional, Sequence, List, Dict

import stackprinter
from jose import jwt
from loguru import logger

from src.aggregator.DTOs import UserSchema
from src.aggregator.DTOs.olympiad import OlympiadSchema, OlympiadSchemaCard
from src.aggregator.database import crud, Olympiad
from src.setup import settings, get_session_maker


def logging_wrapper(func):
    """
    Decorator for loguru
    Contextualizes loguru and allows loguru to catch errors

    Args:
        func: function to be logged

    Returns: wrapper))

    """
    async def wrapper(*args, **kwargs):
        filtered_kwargs = kwargs.copy()
        filtered_kwargs.pop('db_session', None)
        with logger.contextualize(**filtered_kwargs), logger.catch():
            return await func(*args, **kwargs)

    return wrapper


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token (JWT) with the provided data.

    This function creates a JSON Web Token (JWT) with the given data and an expiration time.
    The expiration time is either provided as a `timedelta` or set to a default of 15 minutes.
    The token is encoded using the secret key and algorithm specified in the application settings.

    Args:
        data (dict): The data to be encoded in the JWT payload.
        expires_delta (Optional[timedelta]): The time delta after which the token will expire. If not provided, a default of 15 minutes is used.

    Returns:
        str: The encoded JWT as a string.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.encryption.secret_key, algorithm=settings.encryption.algorithm)

    logger.info('Generated access token')
    return encoded_jwt


async def decode_access_token(access_token: str) -> Optional[str]:
    """
    Decode an access token (JWT) and return the username.

    This function decodes a JSON Web Token (JWT) using the application's secret key and algorithm.
    It extracts the 'sub' (subject) claim from the payload, which should contain the username.
    If the token is valid and contains a username, it returns the username. Otherwise, it returns None.

    Args:
        access_token (str): The encoded JWT to be decoded.

    Returns:
        Optional[str]: The username extracted from the token payload, or None if the token is invalid or does not contain a username.
    """
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
async def send_email(email_server: smtplib.SMTP_SSL, receiver_email: str, body: str) -> None:
    """
    Send an email using the provided SMTP server.

    Args:
        email_server (smtplib.SMTP_SSL): An instance of the SMTP_SSL class from the smtplib module, representing the SMTP server to use for sending the email.
        receiver_email (str): The email address of the recipient.
        body (str): The body of the email message.

    Returns:
        None
    """
    email_server.sendmail(settings.stmp.name, receiver_email, body)

    logger.info(f'Sent email to {receiver_email}')


async def database_sink(message) -> None:
    """
    Loguru sink function to write log records to the database.

    This function is a sink for loguru, which means it is called by loguru whenever a log record is created.
    The function retrieves the user ID, log level, log message, and exception (if any) from the log record.
    It then determines the appropriate log type based on the log level and user ID. Finally, it writes the log
    record to the database using the `crud.add_log` function.

    Note:
        This function assumes the existence of the `crud.add_log` function and the `LogTypes` enum.

    Args:
        message (loguru.Record): The log record created by loguru.

    Returns:
        None
    """
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
        session=session_maker(),
        user_id=user_id,
        log_type=log_type.value,
        date=datetime.now(),
        text=text)


async def get_nearest_date(olympiad: OlympiadSchema) -> datetime:
    """
    Helper function for getting nearest stage date for olympiad

    Args:
        olympiad: olympiad for what we need to get stage date

    Returns: nearest stage date

    """
    now = datetime.now()

    for dates in olympiad.dates.values():
        temp = datetime.strptime(dates[0], '%Y-%m-%d')
        if now < temp:
            return temp


async def get_nearest_date_str(olympiad: OlympiadSchema) -> str:
    """
    Helper function for getting nearest stage date for olympiad

    Args:
        olympiad: olympiad for what we need to get stage date

    Returns: formatted string with nearest stage date for frontend

    """
    now = datetime.now()

    for stage, dates in olympiad.dates.items():
        temp = datetime.strptime(dates[0], '%Y-%m-%d')
        if now < temp:
            return f'{stage} - {temp.strftime("%b %d")}'


async def humanize_classes(olympiad: OlympiadSchema) -> str:
    """
    Makes grades list into readable string

    Args:
        olympiad: olympiad which grades should be humanized

    Returns: formatted grades string for backend

    """
    classes = ''
    if len(olympiad.classes) == 1:
        classes = f'{olympiad.classes[1]} класс'
    else:
        classes = f'{min(olympiad.classes)} - {max(olympiad.classes)} классы'

    return classes


async def optimize_subjects(olympiad: OlympiadSchema) -> str:
    """
    Optimizing subjects for frontend
    Accumulates all language olympiads into one naming

    Args:
        olympiad: olympiad which subject to optimize

    Returns: optimized subjects

    """
    language_flag = 0
    subjects = ''

    for subject in olympiad.subjects:
        if 'язык' in subject.lower():
            language_flag = 1
        else:
            subjects += f'{subject}' + ', '

    if language_flag is True:
        subjects += 'Языковедение'
    else:
        subjects = subjects[:-2]

    return subjects


class LogTypes(Enum):
    """
    Log types for database logging
    """

    system = 0
    exceptions = 1
    user = 2


async def convert_olympiads_to_view_format(
        olympiads: Sequence[Olympiad],
        auth: UserSchema | bool
) -> List[OlympiadSchemaCard]:
    """
    Converts a sequence of Olympiad objects to a list of OlympiadSchemaCard objects.
    If user is authorized gets from it additional data

    Args:
        olympiads (Sequence[Olympiad]): A sequence of Olympiad objects to be converted.
        auth (UserSchema | bool): A UserSchema object representing the authenticated user, or False if not authenticated.

    Returns:
        List[OlympiadSchemaCard]: A list of OlympiadSchemaCard objects representing the converted olympiads.
    """
    card_olympiads = []
    is_favorite, is_notified, is_participant = False, False, False
    for olympiad in olympiads:
        olympiad = olympiad.to_dto_model()

        if auth is not False:
            is_favorite = olympiad.id in auth.favorites
            is_notified = olympiad.id in auth.notifications
            is_participant = olympiad.id in auth.participates

        card_olympiad = OlympiadSchemaCard(
            id=olympiad.id,
            title=olympiad.title,
            description=olympiad.description,
            date=await get_nearest_date(olympiad),
            datestr=await get_nearest_date_str(olympiad),
            classes=await humanize_classes(olympiad),
            subjects=await optimize_subjects(olympiad),
            is_favorite=is_favorite,
            is_notified=is_notified,
            is_participant=is_participant
        )

        card_olympiads.append(card_olympiad)

    return card_olympiads


async def jsonify_dates(olympiad: OlympiadSchema) -> List[Dict[str, str]]:
    """
    Reformatting stages json for frontend

    Args:
        olympiad: olympiad which grades need to be optimized

    Returns: new json List[Dict[str, str]]

    """
    result = []

    for stage, dates in olympiad.dates.items():
        date_start = datetime.strptime(dates[0], "%Y-%m-%d")
        temp = {'name': stage, 'date_start': date_start.strftime("%b %d")}

        if len(dates) == 2:
            date_end = datetime.strptime(dates[1], "%Y-%m-%d")
            temp['date_end'] = f'- {date_end.strftime("%b %d")}'
        else:
            temp['date_end'] = ''

        result.append(temp.copy())

    return result
