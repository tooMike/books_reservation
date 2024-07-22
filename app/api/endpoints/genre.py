from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_genre_exists,
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.genre import genre_crud
from app.schemas.genre import GenreDB, GenreCreate

router = APIRouter()


@router.post(
    '/',
    response_model=GenreDB,
    # dependencies=[Depends(current_superuser)]
)
async def create_book(
        obj_in: GenreCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создание жанра. Только для суперюзеров."""
    genre = await genre_crud.create(
        obj_in=obj_in,
        session=session,
    )
    return genre


@router.delete(
    '/{book_id}',
    response_model=GenreDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_author(
        genre_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление жанра. Только для суперюзеров."""
    genre = await check_genre_exists(genre_id=genre_id, session=session)
    genre = await genre_crud.remove(db_obj=genre, session=session)
    return genre


@router.get(
    '/',
    response_model=list[GenreDB]
)
async def get_all_authors(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех жанров."""
    genres = await genre_crud.get_multi(session)
    return genres
