from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.book import Book


class Genre(Base):
    """Модель жанра."""

    name: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped['Book'] = relationship(back_populates='genres')

    def __repr__(self):
        return self.name
