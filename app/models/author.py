from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.book import Book


class Author(Base):
    """Автор книги."""

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=False)

    books: Mapped[list['Book']] = relationship(back_populates='author')

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
