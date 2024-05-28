from .models import *


async def initialize_database(engine):
    """
    Function for initialize database

    Args:
        engine: thing needed database to initialize

    Returns:

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
