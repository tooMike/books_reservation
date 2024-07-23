from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_genre_exists, check_genre_name_duplicate
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.genre import genre_crud
from app.schemas.genre import GenreCreate, GenreDB, GenreUpdate

router = APIRouter()


@router.post(
    '/',
    response_model=GenreDB,
    dependencies=[Depends(current_superuser)]
)
async def create_genre(
        genre: GenreCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создание жанра. Только для суперюзеров."""
    await check_genre_name_duplicate(genre_name=genre.name, session=session)
    genre = await genre_crud.create(
        obj_in=genre,
        session=session,
    )
    return genre


@router.delete(
    '/{genre_id}',
    response_model=GenreDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_genre(
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
async def get_all_genres(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех жанров."""
    genres = await genre_crud.get_multi(session=session)
    return genres


@router.patch(
    '/{genre_id}',
    response_model=GenreDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_genre(
        genre_id: int,
        obj_in: GenreUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменение жанра. Только для суперюзеров."""
    genre = await check_genre_exists(
        genre_id=genre_id, session=session
    )

    if genre.name is not None:
        await check_genre_name_duplicate(
            genre_name=obj_in.name,
            session=session
        )

    genre = await genre_crud.update(
        db_obj=genre, obj_in=obj_in, session=session
    )
    return genre
