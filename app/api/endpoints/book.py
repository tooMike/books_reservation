from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_all_genre_exists, check_author_exists,
    check_book_exists,
    check_genre_exists,
)
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.book import book_crud
from app.schemas.book import BookCreate, BookDB, BookUpdate

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
    obj_in_data = obj_in.dict()
    genre_ids = obj_in_data.pop('genres')
    # Проверяем, существуют ли жанры с переданными id
    genres = await check_all_genre_exists(genre_ids=genre_ids, session=session)
    # Проверяем, существует ли автор с переданным id
    await check_author_exists(author_id=obj_in.author_id, session=session)

    book = await book_crud.create_book(
        obj_in=obj_in_data,
        genres=genres,
        session=session,
    )
    return book


@router.delete(
    '/{book_id}',
    response_model=BookDB,
    # dependencies=[Depends(current_superuser)]
)
async def delete_book(
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
async def get_all_books(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех книг."""
    books = await book_crud.get_multi_books(session)
    return books


@router.patch(
    '/{book_id}',
    response_model=BookDB,
    # dependencies=[Depends(current_superuser)],
)
async def partially_update_book(
        book_id: int,
        obj_in: BookUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменение книги. Только для суперюзеров."""
    # Проверяем, что такая книга существует
    book = await check_book_exists(
        book_id=book_id, session=session
    )

    # Проверяем, существует ли автор с переданным id
    if obj_in.author_id is not None:
        await check_author_exists(author_id=obj_in.author_id, session=session)
    # Проверяем, существуют ли жанры с переданными id
    if obj_in.genres is not None:
        genres = await check_all_genre_exists(genre_ids=obj_in.genres, session=session)
        book = await book_crud.update_book(
            db_obj=book, obj_in=obj_in, genres=genres, session=session
        )
    else:
        book = await book_crud.update_book(
            db_obj=book, obj_in=obj_in, session=session
        )
    return book
