from typing import Union, List

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    mail: EmailStr
    password: str
    favorites: List[int]

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    username: str
    mail: EmailStr
    password: str
