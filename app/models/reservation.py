from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.core.db import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
