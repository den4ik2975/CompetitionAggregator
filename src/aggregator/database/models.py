from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, JSON, DateTime, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from src.aggregator.DTOs import UserSchema, NotificationSchema, OlympiadSchema


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {List[int]: JSON()}

    def to_dto_model(self, model):
        return model(**self.__dict__)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str]
    mail: Mapped[str]
    favorites: Mapped[List[int]]
    participate: Mapped[List[int]]
    hashed_password: Mapped[str]

    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")

    def to_dto_model(self, model=UserSchema) -> UserSchema:
        return super().to_dto_model(model)


class Olympiad(Base):
    __tablename__ = "olympiads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str]
    level: Mapped[int | None]
    dates: Mapped[List[datetime]] = mapped_column(JSON)
    description: Mapped[str | None]
    subjects: Mapped[List[int]]
    classes: Mapped[List[int]]
    regions: Mapped[List[int]]
    site_data: Mapped[str | None]

    notifications: Mapped[List["Notification"]] = relationship(back_populates="olympiad")

    def to_dto_model(self, model=OlympiadSchema) -> OlympiadSchema:
        return super().to_dto_model(model)


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    olympiad_id: Mapped[int] = mapped_column(ForeignKey("olympiads.id"))
    date: Mapped[datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="notifications")
    olympiad: Mapped["Olympiad"] = relationship(back_populates="notifications")

    def to_dto_model(self, model=NotificationSchema) -> NotificationSchema:
        return super().to_dto_model(model)


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    log_type: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime)
    text: Mapped[str]


class LogTypes(Enum):
    system = 0
    exceptions = 1
    user = 2