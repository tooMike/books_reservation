from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_author_exists,
    check_book_exists,
    check_genre_exists,
)
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.book import book_crud
from app.schemas.book import BookCreate, BookDB

router = APIRouter()


@router.post(
    '/',
    response_model=BookDB,
    # dependencies=[Depends(current_superuser)]
)
async def create_book(
        obj_in: BookCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создание книги. Только для суперюзеров."""
    # Проверяем, существует ли жанр с переданным id
    await check_genre_exists(genre_id=obj_in.genre_id, session=session)
    # Проверяем, существует ли автор с переданным id
    await check_author_exists(author_id=obj_in.author_id, session=session)
    book = await book_crud.create(
        obj_in=obj_in,
        session=session,
    )
    return book


@router.delete(
    '/{book_id}',
    response_model=BookDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_author(
        book_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление автора. Только для суперюзеров."""
    book = await check_book_exists(book_id=book_id, session=session)
    book = await book_crud.remove(db_obj=book, session=session)
    return book


@router.get(
    '/',
    response_model=list[BookDB]
)
async def get_all_authors(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех книг."""
    books = await book_crud.get_multi(session)
    return books
