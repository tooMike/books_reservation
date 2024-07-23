import asyncio
from datetime import datetime

from sqlalchemy import select

from app.celery_worker import app
from app.core.db import AsyncSessionLocal, get_async_session
from app.models import Reservation


@app.task
def remove_expired_reservations():
    """Синхронная функция для работы Celery"""
    asyncio.run(remove_expired_reservations_async())


async def remove_expired_reservations_async():
    """Асинхронная функция для удаления истекших бронирований."""
    async with AsyncSessionLocal() as session:
        current_time = datetime.utcnow()
        result = await session.execute(
            select(Reservation).where(Reservation.end_time < current_time)
        )
        expired_reservations = result.scalars().all()

        for reservation in expired_reservations:
            await session.delete(reservation)
        await session.commit()
