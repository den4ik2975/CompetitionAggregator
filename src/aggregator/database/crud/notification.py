from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.database import Notification


# ------------------ Add ------------------
async def add_notification(
        session: async_session,
        user_id: int,
        olympiad_id: int,
        text: str,
        date: datetime
):
    notification = Notification(
        user_id=user_id,
        olympiad_id=olympiad_id,
        text=text,
        date=date,
    )

    session.add(notification)
    await session.commit()


# ------------------ Get ------------------
async def get_all_notifications(
        session: async_session,
) -> Sequence[Notification]:
    stmt = select(Notification)
    notifications = await session.scalars(stmt)

    return notifications.all()


async def get_limited_notifications(
        session: async_session,
        start: int,
        end: int,
) -> Sequence[Notification]:
    stmt = select(Notification).where(Notification.id.between(start, end))
    notifications = await session.execute(stmt)

    return notifications.scalars().all()


async def get_notification_by_id(
        session: async_session,
        notification_id: int,
) -> Notification | None:
    stmt = select(Notification).where(Notification.id == notification_id)
    notification = await session.scalar(stmt)

    return notification


async def get_notifications_by_user_and_olympiad_id(
        session: async_session,
        user_id: int,
        olympiad_id: int,
) -> Sequence[Notification]:
    stmt = select(Notification).where(Notification.user_id == user_id).where(
        Notification.olympiad_id == olympiad_id)
    notifications = await session.scalars(stmt)

    return notifications.all()


# ------------------ Update ------------------


# ------------------ Delete ------------------
async def delete_notification_by_id(
        session: async_session,
        notification_id: int
) -> Notification | None:
    notification = await get_notification_by_id(session=session, notification_id=notification_id)

    await session.delete(notification)

    return notification


async def delete_notifications_by_user_and_olympiad_id(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> bool:
    notifications = await get_notifications_by_user_and_olympiad_id(session=session,
                                                                    user_id=user_id,
                                                                    olympiad_id=olympiad_id)

    for notification in notifications:
        session.delete(notification)

    return True
