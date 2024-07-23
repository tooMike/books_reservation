from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.author import Author
    from app.models.reservation import Reservation


book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", ForeignKey("book.id")),
    Column("genre", ForeignKey("genre.id")),
)


class Book(Base):
    """Модель книги."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float)
    pages: Mapped[int] = mapped_column(Integer)
    genres: Mapped[list['Genre']] = relationship(
        secondary=book_genre_association, back_populates="books"
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('author.id'))
    author: Mapped['Author'] = relationship(back_populates='books')

    reservation: Mapped['Reservation'] = relationship(back_populates='book')

    def __repr__(self):
        return self.name
