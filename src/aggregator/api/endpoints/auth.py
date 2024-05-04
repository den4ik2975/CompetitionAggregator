from typing import Annotated, List

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.aggregator.service_layer import services
from src.aggregator.api import session_service
from src.aggregator.DTOs import UserSchemaAdd


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)





