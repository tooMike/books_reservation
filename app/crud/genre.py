from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Genre


class CRUDGenre(CRUDBase):
    """Класс CRUD для жанров."""

    async def get_genre_id_by_name(
            self,
            genre_name: str,
            session: AsyncSession,
    ) -> int | None:
        """Получение id жанра по названию"""
        genre_id = await session.execute(
            select(Genre.id).where(
                Genre.name == genre_name
            )
        )
        genre_id = genre_id.scalars().first()
        return genre_id

    async def get_genres_by_list_ids(
            self,
            genre_ids: list[int],
            session: AsyncSession,
    ) -> list[Genre]:
        """Получение списка жанров по списку переданных id"""
        genres = await session.execute(
            select(Genre).where(Genre.id.in_(genre_ids))
        )
        return genres.scalars().all()



genre_crud = CRUDGenre(Genre)
