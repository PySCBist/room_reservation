from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_meeting_room_exists,
                                check_reservation_intersections,
                                check_reservation_before_edit)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User
from app.crud.reservation import reservation_crud
from app.schemas.reservation import (ReservationCreate,
                                     ReservationUpdate,
                                     ReservationDB)

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(reservation: ReservationCreate,
                             session: AsyncSession = Depends(
                                 get_async_session),
                             user: User = Depends(current_user),
                             ):
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(**reservation.dict(),
                                          session=session)
    new_reservation = await reservation_crud.create(
        reservation, session, user
    )
    return new_reservation


@router.get('/', response_model=list[ReservationDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров."""
    all_reservations = await reservation_crud.get_multi(session)
    return all_reservations


@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
        reservation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, user, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, user, session)
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session)
    reservation = await reservation_crud.update(reservation, obj_in, session)
    return reservation


@router.get('/my_reservations', response_model=list[ReservationDB],
            # Добавляем множество с полями, которые надо исключить из ответа.
            response_model_exclude={'user_id'})
async def get_my_reservations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех бронирований для текущего пользователя."""
    reservations = await reservation_crud.get_by_user(user, session)
    return reservations
