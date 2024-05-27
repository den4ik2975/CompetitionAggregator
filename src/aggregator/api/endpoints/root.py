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
    logger.info('Request for olympiad search')

    if search is not None:
        olympiads = await services.search_olympiads(auth=auth,
                                                    search_string=search,
                                                    db_session=db_session)

    elif subjects is not None or grades is not None:
        olympiads = await services.filter_olympiads(subjects=subjects,
                                                    grades=grades,
                                                    auth=auth,
                                                    db_session=db_session)

    else:
        olympiads = await services.get_olympiads(auth=auth,
                                                 db_session=db_session
                                                 )

    if sortBy is not None:
        olympiads = await services.sort_olympiads(sort_clause=sortBy,
                                                  olympiads=olympiads)

    return olympiads
