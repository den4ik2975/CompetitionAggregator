from pydantic import BaseModel


class CommentSchema(BaseModel):
    id: int
    user_id: int
    olympiad_id: int
    text: str

    class Config:
        from_attributes = True


class CommentSchemaAdd(BaseModel):
    user_id: int
    olympiad_id: int
    text: str

    class Config:
        from_attributes = True