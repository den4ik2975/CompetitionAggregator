from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .models import *


async def initialize_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session_maker(connection_string) -> async_sessionmaker:
    engine = create_async_engine(connection_string)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    await initialize_database(engine)

    return session_maker
