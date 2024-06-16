from pydantic import BaseModel, validator, root_validator
from datetime import datetime


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


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

    class Config:
        orm_mode = True
