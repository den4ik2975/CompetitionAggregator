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
    """
    Retrieves information about a specific Olympiad.

    Args:
        olympiad_id (int): The ID of the Olympiad to retrieve.
        auth (UserSchema | bool): The authenticated user information or a boolean value
            indicating if the user is authenticated or not. Obtained from the `get_auth`
            dependency.
        db_session (async_session): An asynchronous database session obtained from the
            `get_db_session` dependency.

    Returns:
        OlympiadSchemaView: A representation of the requested Olympiad.
    """

    logger.info('Request for single olympiad')

    olympiad = await services.get_olympiad(olympiad_id=olympiad_id,
                                           auth=auth,
                                           db_session=db_session)

    return olympiad
