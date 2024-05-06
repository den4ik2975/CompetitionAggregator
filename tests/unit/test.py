import asyncio

from src.aggregator.database import get_session_maker
from src.aggregator.database.crud import *
from src.project_logging import logging_wrapper


async def test():
    date = datetime.now()
    strr = 'sqlite+aiosqlite:///data.db'
    # await add_notification(await get_session_maker(strr), 1, 2, date)
    # await add_user(await get_session_maker(strr))

    ntfs = await get_all_notifications(await get_session_maker(strr))
    print(ntfs)
    for ntf in ntfs:
        print(ntf.id)





