from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.crud.genre import genre_crud
from app.models import Book, Genre, User
from app.schemas.book import BookDB


class CRUDBook(CRUDBase):
    """Класс CRUD операций для книг."""
    async def create_book(
            self,
            obj_in: dict,
            genres: list[Genre],
            session: AsyncSession,
    ):
        """Создание книги."""
        book = self.model(**obj_in)
        book.genres = genres

        session.add(book)
        await session.commit()
        await session.refresh(book)
        # Подгружаем связанные жанры для правильного формирования ответа
        await session.execute(
            select(Book).options(
                selectinload(Book.genres)
            ).where(Book.id == book.id)
        )

        return book


book_crud = CRUDBook(Book)
