from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

# if TYPE_CHECKING:
#     from app.models.group import Group
#     from app.models.users import User
#     from app.models.comment import Comment


class Book(Base):
    """Модель книги."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float)
    pages: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('author.id'))
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genre.id'))

    # user: Mapped['User'] = relationship(back_populates='posts')
    # group: Mapped['Group'] = relationship(back_populates='posts')
    # comments: Mapped['Comment'] = relationship(back_populates='post')

    def __repr__(self):
        return self.name[:25]
