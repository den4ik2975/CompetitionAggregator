from typing import Union, List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    telegram_id: Union[int, None] = None
    name: str
    favorites: List[int]

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    id: int
    telegram_id: Union[int, None] = None
    name: str
    favorites: List[int]
