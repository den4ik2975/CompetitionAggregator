from datetime import datetime

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    id: int
    user_id: int
    olympiad_id: int
    date: datetime

    class Config:
        from_attributes = True


class NotificationSchemaAdd(BaseModel):
    user_id: int
    olympiad_id: int
    date: datetime

    class Config:
        from_attributes = True