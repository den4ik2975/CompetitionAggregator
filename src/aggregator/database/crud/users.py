from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import User


# ------------------ Add ------------------
async def add_user(
        session_maker: async_sessionmaker,
        username: str,
        mail: str,
        password: str,
        favorites: List[int | None] = None
) -> User:
    if favorites is None:
        favorites = []

    user = User(
        username=username,
        mail=mail,
        password=password,
        favorites=favorites,
    )

    async with session_maker() as session:
        session.add(user)
        await session.commit()

        return user


# ------------------ Get ------------------
async def get_user_by_id(
        session_maker: async_sessionmaker,
        user_id: int
) -> User | None:
    async with session_maker() as session:
        stmt = select(User).where(User.id == user_id)
        user = await session.scalar(stmt)

        return user


async def get_user_by_email(
        session_maker: async_sessionmaker,
        mail: str
) -> User | None:
    async with session_maker() as session:
        stmt = select(User).where(User.mail == mail)
        user = await session.scalar(stmt)

        return user


async def get_user_by_username(
        session_maker: async_sessionmaker,
        username: str
) -> User | None:
    async with session_maker() as session:
        stmt = select(User).where(User.username == username)
        user = await session.scalar(stmt)

        return user


# ------------------ Update ------------------
async def update_user(
        session_maker: async_sessionmaker,
        user: User,
        **kwargs
) -> User | None:
    if user is not None:
        for key, value in kwargs.items():
            try:
                getattr(user, key)
                setattr(user, key, value)

            except AttributeError:
                pass

    with session_maker() as session:
        session.add(user)
        await session.commit()

        return user


async def update_user_by_id(
        session_maker: async_sessionmaker,
        user_id: int,
        **kwargs
) -> User | None:
    user = await get_user_by_id(session_maker=session_maker, user_id=user_id)
    updated_user = await update_user(session_maker=session_maker, user=user, **kwargs)
    return updated_user


async def update_user_by_telegram_id(
        session_maker: async_sessionmaker,
        telegram_id: int,
        **kwargs
) -> User | None:
    user = await get_user_by_telegram_id(session_maker=session_maker, telegram_id=telegram_id)
    updated_user = await update_user(session_maker=session_maker, user=user, **kwargs)
    return updated_user


# ------------------ Delete ------------------
async def delete_user_by_id(
        session_maker: async_sessionmaker,
        user_id: int
) -> User | None:
    user = await get_user_by_id(session_maker=session_maker, user_id=user_id)

    with session_maker() as session:
        await session.delete(user)

        return user
