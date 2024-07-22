from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

# if TYPE_CHECKING:
#     from app.models.group import Group
#     from app.models.users import User
#     from app.models.comment import Comment


class Author(Base):
    """Автор книги."""

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[float] = mapped_column(Float)
    avatar: Mapped[Optional[str]] = mapped_column(String)


    # user: Mapped['User'] = relationship(back_populates='posts')
    # group: Mapped['Group'] = relationship(back_populates='posts')
    # comments: Mapped['Comment'] = relationship(back_populates='post')

    def __repr__(self):
        return f"{self.name} {self.surname}"
