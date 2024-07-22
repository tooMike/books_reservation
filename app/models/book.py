from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.author import Author


class Book(Base):
    """Модель книги."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float)
    pages: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('author.id'))
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genre.id'))

    author: Mapped['Author'] = relationship(back_populates='books')
    genres: Mapped['Genre'] = relationship(back_populates='books')

    def __repr__(self):
        return self.name
