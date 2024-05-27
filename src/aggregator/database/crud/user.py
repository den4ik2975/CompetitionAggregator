from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm.attributes import flag_modified

from src.aggregator.database import User


# ------------------ Add ------------------
async def add_user(
        session: async_session,
        username: str,
        mail: str,
        password: str,
        favorites: List[int | None] = None,
        participates: List[int | None] = None,
        notifications: List[int | None] = None
) -> User:
    if favorites is None:
        favorites = []

    if participates is None:
        participates = []

    if notifications is None:
        notifications = []

    user = User(
        username=username,
        mail=mail,
        hashed_password=password,
        favorites=favorites,
        n=7,
        participates=participates,
        notifications=notifications,
    )

    session.add(user)
    await session.commit()

    return user


# ------------------ Get ------------------
async def get_user_by_id(
        session: async_session,
        user_id: int
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)

    return user


async def get_user_by_email(
        session: async_session,
        mail: str
) -> User | None:
    stmt = select(User).where(User.mail == mail)
    user = await session.scalar(stmt)

    return user


async def get_user_by_username(
        session: async_session,
        username: str
) -> User | None:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)

    return user


# ------------------ Update ------------------
async def update_user_favorites(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None and olympiad_id not in user.favorites:
        user.favorites.append(olympiad_id)
        flag_modified(user, 'favorites')
        session.add(user)
        await session.commit()

        return user


async def update_user_participate(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None and olympiad_id not in user.participates:
        user.participates.append(olympiad_id)

        flag_modified(user, 'participates')
        session.add(user)
        await session.commit()

        return user


async def update_user_notification(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None and olympiad_id not in user.notifications:
        user.notifications.append(olympiad_id)

        flag_modified(user, 'notifications')
        session.add(user)
        await session.commit()

        return user


async def update_user_n(
        session: async_session,
        user_id: int,
        n: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None:
        user.n = n

        session.add(user)
        await session.commit()

        return user


# ------------------ Delete ------------------
async def delete_user_by_id(
        session: async_session,
        user_id: int
) -> User | None:
    user = await get_user_by_id(session=session, user_id=user_id)

    await session.delete(user)

    return user


async def delete_user_favorite(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None and olympiad_id in user.favorites:
        user.favorites.remove(olympiad_id)

        flag_modified(user, 'favorites')
        session.add(user)
        await session.commit()

        return user


async def delete_user_participate(
        session: async_session,
        user_id: int,
        olympiad_id: int
) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user is not None and olympiad_id in user.participates:
        user.favorites.remove(olympiad_id)

        flag_modified(user, 'participates')
        session.add(user)
        await session.commit()

        return user
