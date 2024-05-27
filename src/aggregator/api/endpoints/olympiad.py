from typing import Annotated

from fastapi import APIRouter, Depends, Path
from loguru import logger
from sqlalchemy.ext.asyncio import async_session

from src.aggregator.DTOs import UserSchema, OlympiadSchemaView
from src.aggregator.api.dependencies import get_db_session, get_auth
from src.aggregator.service_layer import services

router_olympiad = APIRouter(
    prefix="/olympiad",
    tags=["Olympiad"],
)


@router_olympiad.get("/{olympiad_id}")
async def get_olympiad(
        olympiad_id: Annotated[int, Path()],
        auth: Annotated[UserSchema | bool, Depends(get_auth)],
        db_session: Annotated[async_session, Depends(get_db_session)],
) -> OlympiadSchemaView:
    logger.info('Request for single olympiad')

    olympiad = await services.get_olympiad(olympiad_id=olympiad_id,
                                           auth=auth,
                                           db_session=db_session)

    return olympiad
