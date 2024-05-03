import asyncio
from database.connection import get_session_maker

loop = asyncio.get_event_loop()
loop.run_until_complete(get_session_maker('sqlite+aiosqlite:///data.db'))
