from typing import List, Annotated

from fastapi import APIRouter, Depends, Query
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import OlympiadSchemaView, UserSchema
from src.aggregator.api.dependencies import get_db_session, get_auth
from src.aggregator.service_layer import services

router_root = APIRouter(
    prefix="",
    tags=["Root"],
)


@router_root.get("/")
async def get_olympiads(
        search: Annotated[str, Query()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> List[OlympiadSchemaView]:
    logger.info('Request for olympiad cards')

    olympiads = await services.search_olympiads(auth=auth,
                                                search_string=search,
                                                db_session=db_session)

    return olympiads


@router_root.get("/")
async def get_olympiads(
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> List[OlympiadSchemaView]:
    logger.info('Request for olympiad cards')

    olympiads = await services.get_olympiads(auth=auth,
                                             db_session=db_session)

    return olympiads
