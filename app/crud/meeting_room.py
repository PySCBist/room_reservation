from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


async def create_meeting_room(new_room: MeetingRoomCreate) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)

    async with AsyncSessionLocal() as session:
        session.add(db_room)

        await session.commit()  # Записываем изменения непосредственно в БД.
        await session.refresh(db_room)  # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.

    return db_room


async def get_room_id_by_name(room_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(MeetingRoom.name == room_name))

        db_room_id = db_room_id.scalars().first()

    return db_room_id
