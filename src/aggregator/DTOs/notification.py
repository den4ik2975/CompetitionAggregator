from datetime import datetime

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    """
    Pydantic class that mirrors Notification from SQLAlchemy tables

    Attributes:
        id: notification id
        user_id: user id notification belongs to
        olympiad_id: olympiad id notification belongs to
        date: date when notification meant to be sent
    """

    id: int
    user_id: int
    olympiad_id: int
    date: datetime

    class Config:
        from_attributes = True