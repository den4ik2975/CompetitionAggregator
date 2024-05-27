from typing import List

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    mail: EmailStr
    hashed_password: str
    n: int
    favorites: List[int]
    participates: List[int]
    notifications: List[int]

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    username: str
    mail: EmailStr
    password: str


class UserSchemaAuth(BaseModel):
    login: str | EmailStr
    password: str
