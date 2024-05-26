from datetime import datetime
from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import Olympiad


# ------------------ Add ------------------
async def add_olympiad(
        session_maker: async_sessionmaker,
        title: str,
        level: int | None = None,
        dates: List[datetime] = None,
        description: str | None = None,
        subjects: List[int] = None,
        classes: List[int] = None,
        regions: List[int] = None,
        site_data: str | None = None,

) -> Olympiad:
    if regions is None:
        regions = []
    if classes is None:
        classes = []
    if subjects is None:
        subjects = []
    if dates is None:
        dates = []

    olympiad = Olympiad(
        title=title,
        level=level,
        dates=dates,
        description=description,
        subjects=subjects,
        classes=classes,
        regions=regions,
        site_data=site_data,
    )

    async with session_maker() as session:
        session.add(olympiad)
        await session.commit()

        return olympiad


# ------------------ Get ------------------
async def get_olympiad_by_id(
        session_maker: async_sessionmaker,
        olympiad_id: int
) -> Olympiad | None:
    async with session_maker() as session:
        stmt = select(Olympiad).where(Olympiad.id == olympiad_id)
        olympiad = await session.scalar(stmt)

    return olympiad


async def get_all_olympiads(
        session_maker: async_sessionmaker,
) -> Sequence[Olympiad]:
    async with session_maker() as session:
        stmt = select(Olympiad).order_by(Olympiad.id)
        olympiads = await session.scalars(stmt)

        return olympiads.all()


async def search_for_olympiads(
        session_maker: async_sessionmaker,
        search_string: str
) -> Sequence[Olympiad]:
    async with session_maker() as session:
        ...


# ------------------ Update ------------------
async def update_olympiad(
        session_maker: async_sessionmaker,
        olympiad: Olympiad,
        **kwargs
) -> Olympiad | None:
    if olympiad is not None:
        for key, value in kwargs.items():
            try:
                getattr(olympiad, key)
                setattr(olympiad, key, value)

            except AttributeError:
                pass

    with session_maker() as session:
        session.add(olympiad)
        await session.commit()

        return olympiad


async def update_olympiad_by_id(
        session_maker: async_sessionmaker,
        olympiad_id: int,
        **kwargs
) -> Olympiad | None:
    olympiad = await get_olympiad_by_id(session_maker=session_maker, olympiad_id=olympiad_id)
    updated_olympiad = await update_olympiad(session_maker=session_maker, olympiad=olympiad, **kwargs)
    return updated_olympiad


# ------------------ Delete ------------------
async def delete_olympiad_by_id(
        session_maker: async_sessionmaker,
        olympiad_id: int
) -> Olympiad | None:
    olympiad = await get_olympiad_by_id(session_maker=session_maker, olympiad_id=olympiad_id)

    with session_maker() as session:
        await session.delete(olympiad)

        return olympiad
