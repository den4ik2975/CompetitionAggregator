from typing import List

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.database import crud
from src.project_logging import logging_wrapper
from src.aggregator.DTOs import OlympiadSchema


@logging_wrapper
async def get_olympiad(olympiad_id: int, user_id: int, session_maker: async_sessionmaker):
    olympiad = crud.get_olympiad_by_id(session_maker=session_maker, olympiad_id=olympiad_id)


@logging_wrapper
async def get_olympiads(session_maker: async_sessionmaker) -> List[OlympiadSchema]:
    olympiads = await crud.get_all_olympiads(session_maker=session_maker)
    olympiads_to_pyd = [olympiad.to_pydantic_model() for olympiad in olympiads]

    return olympiads_to_pyd

