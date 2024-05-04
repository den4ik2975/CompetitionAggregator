from src.aggregator.database.connection import get_session_maker
from src.config import Settings


def session_service():
    return get_session_maker(Settings.database.connection_string)
