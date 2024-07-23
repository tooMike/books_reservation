from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    reservations: Mapped[list['Reservation']] = relationship(
        back_populates='user'
    )
