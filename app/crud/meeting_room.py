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
