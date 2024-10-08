from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.core.db import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    user_id = Column(Integer, ForeignKey('user.id',
                                         name='fk_reservation_user_id_user'))

    def __repr__(self):
        return f'Уже забронировано c {self.from_reserve} по {self.to_reserve}'
