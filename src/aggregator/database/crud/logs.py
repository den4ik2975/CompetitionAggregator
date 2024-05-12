from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import Logs


# ------------------ Add ------------------
async def add_log(
        session_maker: async_sessionmaker,
        user_id: int,
        log_type: int,
        date: datetime,
        text: str
) -> Logs:
    user = Logs(
        user_id=user_id,
        log_type=log_type,
        date=date,
        text=text
    )

    async with session_maker() as session:
        session.add(user)
        await session.commit()

        return user
