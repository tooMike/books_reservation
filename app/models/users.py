from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String

from app.core.db import Base

# if TYPE_CHECKING:
#     from app.models.post import Post
#     from app.models.comment import Comment


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String)

    # posts: Mapped[List['Post']] = relationship(back_populates='user')
    # comments: Mapped[List['Comment']] = relationship(back_populates='user')
