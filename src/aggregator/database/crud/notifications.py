from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import Notification


# ------------------ Add ------------------
async def add_notification(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int,
        date: datetime
) -> Notification:
    notification = Notification(
        user_id=user_id,
        olympiad_id=olympiad_id,
        date=date,
    )

    async with session_maker() as session:
        session.add(notification)
        await session.commit()

        return notification


# ------------------ Get ------------------
async def get_all_notifications(
        session_maker: async_sessionmaker,
) -> Sequence[Notification]:
    async with session_maker() as session:
        stmt = select(Notification)
        notifications = await session.scalars(stmt)

        return notifications.all()


async def get_limited_notifications(
        session_maker: async_sessionmaker,
        start: int,
        end: int,
) -> Sequence[Notification]:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.id.between(start, end))
        notifications = await session.execute(stmt)

        return notifications.scalars().all()


async def get_notification_by_id(
        session_maker: async_sessionmaker,
        notification_id: int,
) -> Notification | None:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.id == notification_id)
        notification = await session.scalar(stmt)

        return notification


async def get_notifications_by_user_and_olympiad_id(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int,
) -> Sequence[Notification]:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.user_id == user_id).where(
            Notification.olympiad_id == olympiad_id)
        notifications = await session.scalars(stmt)

        return notifications.all()


# ------------------ Update ------------------


# ------------------ Delete ------------------
async def delete_notification_by_id(
        session_maker: async_sessionmaker,
        notification_id: int
) -> Notification | None:
    notification = await get_notification_by_id(session_maker=session_maker, notification_id=notification_id)

    with session_maker() as session:
        await session.delete(notification)

        return notification


async def delete_notifications_by_user_and_olympiad_id(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int
) -> bool:
    notifications = await get_notifications_by_user_and_olympiad_id(session_maker=session_maker,
                                                                    user_id=user_id,
                                                                    olympiad_id=olympiad_id)

    with session_maker() as session:
        for notification in notifications:
            session.delete(notification)

        return True
