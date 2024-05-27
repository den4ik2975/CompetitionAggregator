from datetime import datetime

from sqlalchemy.ext.asyncio import async_session

from src.aggregator.database import Logs


# ------------------ Add ------------------
async def add_log(
        session: async_session,
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

    session.add(user)
    await session.commit()

    return user
