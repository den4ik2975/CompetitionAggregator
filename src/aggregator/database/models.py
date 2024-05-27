import json
from datetime import datetime
from typing import List, Dict

from sqlalchemy import ForeignKey, DateTime, TypeDecorator, TEXT
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from src.aggregator.DTOs import UserSchema, NotificationSchema, OlympiadSchema


class UnicodeText(TypeDecorator):
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return str(value)


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {List[int]: JSON(),
                           List[str]: UnicodeText}

    def to_dto_model(self, model):
        if model is None:
            return None
        return model(**self.__dict__)

    def convert_json_fields(self):
        for col_name, col_type in self.__mapper__.c.items():
            if isinstance(col_type.type, UnicodeText):
                json_value = getattr(self, col_name)
                if json_value is not None:
                    setattr(self, col_name, json.loads(json_value.replace("'", '"')))


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
    dates: Mapped[Dict[str, List[str]]] = mapped_column(UnicodeText)
    description: Mapped[str | None]
    subjects: Mapped[List[str]]
    classes: Mapped[List[int]]
    site_data: Mapped[str | None]

    def to_dto_model(self, model=OlympiadSchema) -> OlympiadSchema:
        return super().to_dto_model(model)

    @hybrid_method
    def search_string(self):
        return (' '.join([self.title or ''] + self.subjects)).lower()


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
