from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.service_layer import services
from src.aggregator.api import CommentSchemaAdd, session_service


comment_router = APIRouter(
    prefix="/comment",
    tags=["Comment"],
)


@comment_router.post("")
async def create_comment(comment: CommentSchemaAdd,
                         session_maker: Annotated[async_sessionmaker, Depends(session_service)]):
    dict_comment = comment.model_dump()
    await services.add_comment(**dict_comment)


