import sys

import stackprinter
from loguru import logger

from src.aggregator.database import crudd
from src.aggregator.database.models import LogTypes


def logging_wrapper(func):
    async def wrapper(*args, **kwargs):
        with logger.contextualize(**kwargs), logger.catch():
            return await func(*args, **kwargs)
    return wrapper


def database_sink(message):
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

    crudd.add_log(user_id, log_type, text)


logger.remove()
# logger.add(
#     database_sink,
#     format="[{time:YYYY-MM-DD HH:mm:ss}] ({extra[user_id]:^12} | <b><level>{extra[name]:^18}</level></b>) → {message}\n{exception}",
#     backtrace=True,
#     diagnose=True,
#     level=("INFO"),
# )
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