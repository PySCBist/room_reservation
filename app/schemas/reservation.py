from typing import Optional

from pydantic import BaseModel, validator, root_validator, Extra, Field
from datetime import datetime, timedelta


FROM_TIME = (datetime.now() +
             timedelta(minutes=10)).isoformat(timespec='minutes')
TO_TIME = (datetime.now() +
           timedelta(hours=1)).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        # запретить пользователю передавать параметры, не описанные в схеме
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['to_reserve'] <= values['from_reserve']:
            raise ValueError('Время начала бронирования '
                             'должно быть позже времени окончания!')
        return values

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, from_reserve: datetime):
        if from_reserve <= datetime.now():
            raise ValueError('Время начала бронирования не должно быть'
                             'меньше текущего времени!')
        return from_reserve


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        # Схема может принимать на вход объект базы данных (для response_model = MeetingRoomDB)
        orm_mode = True
