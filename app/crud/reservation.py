from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            book_id: int,
            reservation_id: int | None = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.book_id == book_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_book(
            self,
            book_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.book_id == book_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        return reservations.scalars().all()

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user.id)
        )
        return reservations.scalars().all()


reservation_crud = CRUDReservation(Reservation)
