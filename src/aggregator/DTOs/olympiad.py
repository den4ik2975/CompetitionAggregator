from datetime import datetime
from typing import Union, List, Dict

from pydantic import field_validator, BaseModel


class OlympiadSchema(BaseModel):
    id: int
    title: str
    level: Union[int, None] = None
    dates: List[datetime]
    description: str
    subjects: List[str]
    classes: List[int]
    region: str
    comments: Dict[int, str]

    class Config:
        from_attributes = True

    @field_validator('level')
    @classmethod
    def check_level(cls, v):
        if v not in [None, 1, 2, 3]:
            raise ValueError('Must be None or int from 1 to 3')
        return v


class OlympiadSchemaAdd(BaseModel):
    title: str
    level: Union[int, None] = None
    dates: List[datetime]
    description: str
    subjects: List[str]
    classes: List[int]
    region: str
    comments: Dict[int, str]

    class Config:
        from_attributes = True

    @field_validator('level')
    @classmethod
    def check_level(cls, v):
        if v not in [None, 1, 2, 3]:
            raise ValueError('Must be None or int from 1 to 3')
        return v