from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.book import Book


class Reservation(Base):
    """Модель бронирования."""

    from_reserve: Mapped[DateTime] = mapped_column(DateTime)
    to_reserve: Mapped[DateTime] = mapped_column(DateTime)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('book.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='reservations')
    book: Mapped['Book'] = relationship(back_populates='reservation')

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
