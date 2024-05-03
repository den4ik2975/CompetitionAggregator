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


async def get_notification_by_id(
        session_maker: async_sessionmaker,
        notification_id: int,
) -> Notification | None:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.id == notification_id)
        notification = await session.scalar(stmt)

        return notification


async def get_notifications_by_user_id(
        session_maker: async_sessionmaker,
        user_id: int,
) -> Sequence[Notification]:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.user_id == user_id)
        notifications = await session.scalars(stmt)

        return notifications.all()


async def get_notifications_by_olympiad_id(
        session_maker: async_sessionmaker,
        olympiad_id: int,
) -> Sequence[Notification]:
    async with session_maker() as session:
        stmt = select(Notification).where(Notification.olympiad_id == olympiad_id)
        notifications = await session.scalars(stmt)

        return notifications.all()


# ------------------ Update ------------------
async def update_notification(
        session_maker: async_sessionmaker,
        notification: Notification,
        **kwargs
) -> Notification | None:
    if notification is not None:
        for key, value in kwargs.items():
            try:
                getattr(notification, key)
                setattr(notification, key, value)

            except AttributeError:
                pass

    with session_maker() as session:
        session.add(notification)
        await session.commit()

        return notification


async def update_notification_by_id(
        session_maker: async_sessionmaker,
        notification_id: int,
        **kwargs
) -> Notification | None:
    notification = await get_notification_by_id(session_maker=session_maker, notification_id=notification_id)
    updated_notification = await update_notification(session_maker=session_maker, notification=notification, **kwargs)
    return updated_notification


# ------------------ Delete ------------------
async def delete_notification_by_id(
        session_maker: async_sessionmaker,
        notification_id: int
) -> Notification | None:
    notification = await get_notification_by_id(session_maker=session_maker, notification_id=notification_id)

    with session_maker() as session:
        await session.delete(notification)

        return notification
