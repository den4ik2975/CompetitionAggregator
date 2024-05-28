from typing import List

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """
    Pydantic class that mirrors the User SQLAlchemy model

    Attributes:
        id: user unique id
        username: user's username
        mail: user's email address
        hashed_password: user's hashed password
        n: the number of days for which to send notifications (purpose unclear)
        favorites: list of user favorite olympiad ids
        participates: list of user olympiad ids which user participates
        notifications: list of user olympiad ids that the user wants to receive notifications from
    """
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
    """
    Pydantic class representing the data required to add a new user

    Attributes:
        username: user's username
        mail: user's email address
        password: user's password (will be hashed before storing)
    """
    username: str
    mail: EmailStr
    password: str


class UserSchemaAuth(BaseModel):
    """
    Pydantic class representing the data required for user authentication

    Attributes:
        login: user's login, which can be either username or email address
        password: user's password
    """
    login: str | EmailStr
    password: str

