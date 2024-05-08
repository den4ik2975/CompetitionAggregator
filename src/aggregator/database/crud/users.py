from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

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
        hashed_password=password,
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


async def update_user_favorites(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session_maker, user_id)

    if user is not None:
        user.favorites.append(olympiad_id)
        async with session_maker() as session:
            session.add(user)
            await session.commit()

            return user


async def update_user_participate(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session_maker, user_id)

    if user is not None:
        user.participates.append(olympiad_id)
        async with session_maker() as session:
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


# ------------------ Delete ------------------
async def delete_user_by_id(
        session_maker: async_sessionmaker,
        user_id: int
) -> User | None:
    user = await get_user_by_id(session_maker=session_maker, user_id=user_id)

    with session_maker() as session:
        await session.delete(user)

        return user


async def delete_user_favorite(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session_maker, user_id)

    if user is not None:
        try:
            user.favorites.remove(olympiad_id)
            async with session_maker() as session:
                session.add(user)
                await session.commit()

                return user
        except ValueError:
            return None


async def delete_user_participate(
        session_maker: async_sessionmaker,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session_maker, user_id)

    if user is not None:
        try:
            user.favorites.remove(olympiad_id)
            async with session_maker() as session:
                session.add(user)
                await session.commit()

                return user
        except ValueError:
            return None
