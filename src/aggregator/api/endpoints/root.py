from typing import List, Annotated

from fastapi import APIRouter, Depends, Query
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import OlympiadSchemaCard, UserSchema
from src.aggregator.api.dependencies import get_db_session, get_auth
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads(
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
        search: Annotated[str | None, Query()] = None,
        sortBy: Annotated[str | None, Query()] = None,
        subjects: Annotated[List[str] | None, Query()] = None,
        grades: Annotated[List[int] | None, Query()] = None
) -> List[OlympiadSchemaCard]:
    """
    Retrieve a list of olympiads based on search, filter, and sorting criteria.

    Args:
        auth (UserSchema | bool): Authentication data for the user.
        db_session (async_session): Asynchronous database session.
        search (str | None, optional): Search string to filter olympiads by name or description.
        sortBy (str | None, optional): Sort criteria for the olympiad list.
        subjects (List[str] | None, optional): List of subjects to filter olympiads by.
        grades (List[int] | None, optional): List of grades to filter olympiads by.

    Returns:
        List[OlympiadSchemaCard]: List of olympiads matching the search, filter, and sorting criteria.
    """
    logger.info('Request for olympiad search')

    olympiads_search, olympiads_filter, olympiads = [], [], []

    if search is not None:
        olympiads_search = await services.search_olympiads(auth=auth,
                                                           search_string=search,
                                                           db_session=db_session)

    if subjects is not None or grades is not None:
        olympiads_filter = await services.filter_olympiads(subjects=subjects,
                                                           grades=grades,
                                                           auth=auth,
                                                           db_session=db_session)

    if olympiads_search and olympiads_filter:
        olympiads = []
        for olympiad in olympiads_filter:
            if olympiad in olympiads_search:
                olympiads.append(olympiad)
    elif olympiads_search:
        olympiads = olympiads_search
    elif olympiads_filter:
        olympiads = olympiads_filter

    if not olympiads:
        olympiads = await services.get_olympiads(auth=auth,
                                                 db_session=db_session)

    if sortBy is not None:
        olympiads = await services.sort_olympiads(sort_clause=sortBy,
                                                  olympiads=olympiads)

    return olympiads
