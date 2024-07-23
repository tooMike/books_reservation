from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.crud.genre import genre_crud
from app.models import Book, Genre


class CRUDBook(CRUDBase):
    """Класс CRUD операций для книг."""

    async def get_book(
            self,
            book_id: int,
            session: AsyncSession,
    ):
        """Получение книги и связанных жанров."""
        book = await session.execute(
            select(self.model).where(
                self.model.id == book_id
            ).options(selectinload(self.model.genres))
        )
        return book.scalars().first()

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
        # Подгружаем связанные жанры для правильного формирования ответа
        await session.refresh(book, attribute_names=["genres", "author"])
        return book

    async def get_multi_books(self, session: AsyncSession) -> list[Book]:
        """Получение всех книг с предварительной загрузкой связанных данных."""
        result = await session.execute(
            select(self.model).options(
                selectinload(self.model.genres),
            )
        )
        return result.scalars().all()

    async def update_book(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
            genres: list[Genre] | None = None,
    ):
        """Изменение книги."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        # Заменяем в update_data id жанров на объекты модели
        if genres is not None:
            # Подгружаем книгу со связанными жанрами
            book = await book_crud.get_book(book_id=db_obj.id, session=session)
            book.genres = genres

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj, attribute_names=["genres", "author"])
        return db_obj


book_crud = CRUDBook(Book)
