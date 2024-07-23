from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_book_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from app.core.db import get_async_session
from app.core.users import current_superuser, current_user
from app.crud.reservation import reservation_crud
from app.models import User
from app.schemas.reservation import (
    ReservationCreate, ReservationDB,
    ReservationUpdate,
)

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> ReservationDB:
    """Создание бронирования книги."""
    await check_book_exists(
        reservation.book_id, session
    )
    await check_reservation_intersections(
        **reservation.dict(), session=session
    )
    new_reservation = await reservation_crud.create(
        reservation, session, user
    )
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    """Получение списка всех бронирований. Только для суперюзеров"""
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> ReservationDB:
    """
    Удаление бронирования.
    Для суперюзеров или создателей объекта бронирования.
    """
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> ReservationDB:
    """
    Обновление бронирования.
    Для суперюзеров или создателей объекта бронирования.
    """
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        book_id=reservation.book_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session,
    )
    return reservation


@router.get(
    '/{book_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_reservations_for_book(
        book_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> list[ReservationDB]:
    """Получение списка бронирований для указанной книги."""
    await check_book_exists(book_id, session)
    reservations = await reservation_crud.get_future_reservations_for_book(
        book_id=book_id,
        session=session
    )
    return reservations


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> list[ReservationDB]:
    """Получение списка всех бронирований для текущего пользователя."""
    reservations = await reservation_crud.get_by_user(
        session=session,
        user=user
    )
    return reservations
