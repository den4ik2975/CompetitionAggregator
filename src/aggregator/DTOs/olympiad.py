from datetime import datetime
from typing import Union, List, Dict

from pydantic import field_validator, BaseModel


class OlympiadSchema(BaseModel):
    """
    Pydantic class that mirrors the Olympiad SQLAlchemy model

    Attributes:
        id: olympiad unique id
        title: title of the olympiad
        level: difficulty level of the olympiad (optional)
        dates: dictionary containing start and end dates of the olympiad
        description: description of the olympiad (optional)
        subjects: list of subjects associated with the olympiad
        classes: list of class levels associated with the olympiad

    Methods:
        check_level: field validator to ensure the level attribute is either None or an integer from 1 to 3
    """
    id: int
    title: str
    level: Union[int, None] = None
    dates: Dict[str, List[str]]
    description: str | None = None
    subjects: List[str]
    classes: List[int]

    class Config:
        from_attributes = True

    @field_validator('level')
    @classmethod
    def check_level(cls, v):
        if v not in [None, 1, 2, 3]:
            raise ValueError('Must be None or int from 1 to 3')
        return v


class OlympiadSchemaCard(BaseModel):
    """
    Pydantic class representing a simplified view of an Olympiad for a card/list item

    Attributes:
        id: olympiad unique id
        title: title of the olympiad
        date: start date of the olympiad (optional)
        datestr: string representation of the start date (optional)
        description: description of the olympiad (optional)
        classes: string representation of the class levels associated with the olympiad
        subjects: string representation of subjects associated with the olympiad
        is_favorite: boolean indicating if the olympiad is a user favorite
        is_notified: boolean indicating if the user is subscribed for notifications for this olympiad
        is_participant: boolean indicating if the user is a participant in this olympiad
    """
    id: int
    title: str
    date: datetime | None = None
    datestr: str | None = None
    description: str | None = None
    classes: str  # 9-11 классы
    subjects: str  # "First, Second"
    is_favorite: bool = False
    is_notified: bool = False
    is_participant: bool = False


class OlympiadSchemaView(BaseModel):
    """
    Pydantic class representing a detailed view of an Olympiad.
    It is used for provide all information about olympiad on its page on site

    Attributes:
        id: olympiad unique id
        title: title of the olympiad
        level: difficulty level of the olympiad (optional)
        dates: list of dictionaries containing start and end dates of the olympiad
        date: string representation of the start date (optional)
        description: description of the olympiad (optional)
        subjects: list of subjects associated with the olympiad
        classes: string representation of the class levels associated with the olympiad
        is_favorite: boolean indicating if the olympiad is a user favorite
        is_notified: boolean indicating if the user is subscribed for notifications for this olympiad
        is_participant: boolean indicating if the user is a participant in this olympiad

    Methods:
        check_level: field validator to ensure the level attribute is either None or an integer from 0 to 3
    """
    id: int
    title: str
    level: Union[int, None] = None
    dates: List[Dict[str, str]]
    date: str | None = None
    description: str | None = None
    subjects: List[str]
    classes: str
    is_favorite: bool = False
    is_notified: bool = False
    is_participant: bool = False

    @field_validator('level')
    @classmethod
    def check_level(cls, v):
        if v not in [None, 0, 1, 2, 3]:
            raise ValueError('Must be None or int from 0 to 3')
        return v

