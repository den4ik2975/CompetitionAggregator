from typing import List, Sequence, Dict

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm.attributes import flag_modified

from src.aggregator.database import Olympiad


# ------------------ Add ------------------
async def add_olympiad(
        session: async_session,
        title: str,
        level: int | None = None,
        dates: Dict[str, List[str]] = None,
        description: str | None = None,
        subjects: List[str] = None,
        classes: List[int] = None,
        site_data: str | None = None,

) -> Olympiad:
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
        site_data=site_data,
    )

    session.add(olympiad)
    await session.commit()

    return olympiad


# ------------------ Get ------------------
async def get_olympiad_by_id(
        session: async_session,
        olympiad_id: int
) -> Olympiad | None:
    stmt = select(Olympiad).where(Olympiad.id == olympiad_id)
    olympiad = await session.scalar(stmt)

    olympiad.convert_json_fields()

    return olympiad


async def get_all_olympiads(
        session: async_session,
) -> Sequence[Olympiad]:
    stmt = select(Olympiad).order_by(Olympiad.id)
    olympiads = await session.scalars(stmt)

    fixed_olympiads = await olympiad_fixer(olympiads)

    return fixed_olympiads


async def search_for_olympiads(
        session: async_session,
        search_string: str
) -> Sequence[Olympiad]:
    search_query = f"%{search_string.strip().lower()}%"

    stmt = select(Olympiad).where(
        or_(
            func.lower(Olympiad.title).contains(search_query),
            func.lower(Olympiad.subjects).contains(search_query)
        )
    )

    results = await session.scalars(stmt)

    fixed_results = await olympiad_fixer(results)
    return fixed_results


# ------------------ Update ------------------
async def update_olympiad(
        session: async_session,
        olympiad: Olympiad,
        **kwargs
) -> Olympiad | None:
    if olympiad is not None:
        for key, value in kwargs.items():
            try:
                getattr(olympiad, key)
                setattr(olympiad, key, value)
                flag_modified(olympiad, key)

            except AttributeError:
                pass

    session.add(olympiad)
    await session.commit()

    return olympiad


async def update_olympiad_by_id(
        session: async_session,
        olympiad_id: int,
        **kwargs
) -> Olympiad | None:
    olympiad = await get_olympiad_by_id(session=session, olympiad_id=olympiad_id)
    updated_olympiad = await update_olympiad(session=session, olympiad=olympiad, **kwargs)
    return updated_olympiad


# ------------------ Delete ------------------
async def delete_olympiad_by_id(
        session: async_session,
        olympiad_id: int
) -> Olympiad | None:
    olympiad = await get_olympiad_by_id(session=session, olympiad_id=olympiad_id)

    await session.delete(olympiad)

    return olympiad


async def olympiad_fixer(olympiads: Sequence[Olympiad]) -> Sequence[Olympiad]:
    fixed_olympiads = []
    for olympiad in olympiads:
        olympiad.convert_json_fields()
        fixed_olympiads.append(olympiad)

    return fixed_olympiads
