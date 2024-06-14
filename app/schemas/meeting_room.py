from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=3, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError('Нельзя оставлять название '
                             'переговорки пустым!')
        return value


class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True
