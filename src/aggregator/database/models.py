from datetime import datetime
from typing import List, Dict

from sqlalchemy import ForeignKey, JSON, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from src.aggregator.DTOs import UserSchema, NotificationSchema, OlympiadSchema


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {List[int]: JSON(),
                           List[str]: JSON()}

    def to_dto_model(self, model):
        if model is None:
            return None
        return model(**self.__dict__)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str]
    mail: Mapped[str]
    n: Mapped[int]
    favorites: Mapped[List[int]]
    participates: Mapped[List[int]]
    hashed_password: Mapped[str]

    def to_dto_model(self, model=UserSchema) -> UserSchema:
        return super().to_dto_model(model)


class Olympiad(Base):
    __tablename__ = "olympiads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str]
    level: Mapped[int | None]
    dates: Mapped[Dict[str, List[datetime]]] = mapped_column(JSON)
    description: Mapped[str | None]
    subjects: Mapped[List[str]]
    classes: Mapped[List[int]]
    site_data: Mapped[str | None]

    def to_dto_model(self, model=OlympiadSchema) -> OlympiadSchema:
        return super().to_dto_model(model)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    olympiad_id: Mapped[int] = mapped_column(ForeignKey("olympiads.id"))
    date: Mapped[datetime] = mapped_column(DateTime)

    def to_dto_model(self, model=NotificationSchema) -> NotificationSchema:
        return super().to_dto_model(model)


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    log_type: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime)
    text: Mapped[str]
