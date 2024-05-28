import json
from datetime import datetime
from typing import List, Dict

from sqlalchemy import ForeignKey, DateTime, TypeDecorator, TEXT
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from src.aggregator.DTOs import UserSchema, NotificationSchema, OlympiadSchema


class UnicodeText(TypeDecorator):
    """
    This class implement type to save encoding in jsons with russian strings.
    It stringifies of them and this helps us not to lose encoding.
    Separated class needed for detection which fields convert back to json.

    Attributes:
        impl:
        cache_ok:

    Methods:
        process_bind_param(self, value, dialect):
        process_result_value(self, value, dialect):

    """
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """
        Overrides TypeDecorator method

        Args:
            value: value to convert
            dialect:

        Returns: stringified value

        """
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        """
        Overrides TypeDecorator method

        Args:
            value: value to convert
            dialect:

        Returns: stringified value

        """
        if value is None:
            return value
        return str(value)


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class for all SQLAlchemy schemas

    Attributes:
        type_annotation_map: helps SQLAlchemy mapping

    Methods:
        to_dto_model(self, model): converts SQLAlchemy class to corresponding DTO class

        convert_json_fields(self): converts string object from db to json
    """
    type_annotation_map: dict = {List[int]: JSON(),
                                 List[str]: UnicodeText}

    def to_dto_model(self, model):
        """
        Converts SQLAlchemy class to corresponding DTO class

        Args:
            model: DTO model convert to

        Returns: DTO model of SQLAlchemy class

        """
        if model is None:
            return None
        return model(**self.__dict__)

    def convert_json_fields(self):
        """
        Checks if data type of attribute is UnicodeText and if yes converts UnicodeText to json object (python dict)

        Returns: None

        """
        for col_name, col_type in self.__mapper__.c.items():
            if isinstance(col_type.type, UnicodeText):
                json_value = getattr(self, col_name)
                if json_value is not None:
                    setattr(self, col_name, json.loads(json_value.replace("'", '"')))


class User(Base):
    """
    Class for user table

    Attributes:
        __tablename__: sets table name
        id: user unique id
        username: username
        mail: users email
        n: the number of days for which to send notifications
        favorites: list of user favorite olympiad ids
        participates: list of user olympiad ids which user participates
        notifications: list of user olympiad ids that the user wants to receive notifications from
        hashed_password: hashed user password

    Methods:
        to_dto_model(self, model=UserSchema) -> UserSchema: converts SQLAlchemy class into DTO
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str]
    mail: Mapped[str]
    n: Mapped[int]
    favorites: Mapped[List[int]]
    participates: Mapped[List[int]]
    notifications: Mapped[List[int]]
    hashed_password: Mapped[str]

    def to_dto_model(self, model=UserSchema) -> UserSchema:
        """
        Converts SQLAlchemy class into DTO

        Args:
            model: corresponding DTO model. Passed by default

        Returns: Pydantic DTO model

        """
        return super().to_dto_model(model)


class Olympiad(Base):
    """
    Class for olympiad table

    Attributes:
        __tablename__: sets table name
        id: olympiad unique id
        title: title of the olympiad
        level: difficulty level of the olympiad (optional)
        dates: dictionary containing start and end dates of the olympiad
        description: description of the olympiad (optional)
        subjects: list of subjects associated with the olympiad
        classes: list of class levels associated with the olympiad
        site_data: additional data related to the olympiad (optional)

    Methods:
        to_dto_model(self, model=OlympiadSchema) -> OlympiadSchema: converts SQLAlchemy class into DTO
    """

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
        """
        Converts SQLAlchemy class into DTO

        Args:
            model: corresponding DTO model. Passed by default

        Returns: Pydantic DTO model
        """
        return super().to_dto_model(model)


class Notification(Base):
    """
    Class for notification table

    Attributes:
        __tablename__: sets table name
        id: notification unique id
        user_id: id of the user receiving the notification (foreign key to users table)
        olympiad_id: id of the olympiad for which the notification is sent (foreign key to olympiads table)
        text: notification message text
        date: date and time when the notification was sent

    Methods:
        to_dto_model(self, model=NotificationSchema) -> NotificationSchema: converts SQLAlchemy class into DTO
    """
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    olympiad_id: Mapped[int] = mapped_column(ForeignKey("olympiads.id"))
    text: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime)

    def to_dto_model(self, model=NotificationSchema) -> NotificationSchema:
        """
        Converts SQLAlchemy class into DTO

        Args:
            model: corresponding DTO model. Passed by default

        Returns: Pydantic DTO model
        """
        return super().to_dto_model(model)


class Logs(Base):
    """
    Class for logs table

    Attributes:
        __tablename__: sets table name
        id: log unique id
        user_id: id of the user associated with the log (foreign key to users table)
        log_type: type of log entry
        date: date and time when the log entry was created
        text: log entry text

    Methods:
        to_dto_model(self, model=LogSchema) -> LogSchema: converts SQLAlchemy class into DTO
    """
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    log_type: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime)
    text: Mapped[str]
