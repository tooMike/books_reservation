from io import BytesIO

import aiofiles
from fastapi import HTTPException, UploadFile
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.author import author_crud
from app.crud.book import book_crud
from app.crud.genre import genre_crud
from app.crud.reservation import reservation_crud
from app.models import Author, Book, Genre, User
from app.models.reservation import Reservation


async def validate_image(image: UploadFile) -> str:
    """Валидация изображения."""
    try:
        contents = await image.read()

        try:
            Image.open(BytesIO(contents)).verify()
        except (IOError, SyntaxError):
            raise HTTPException(
                status_code=400,
                detail='Файл изображения не корректен, загрузите другое '
                       'изображение'
            )

        # Запишем файл на диск
        file_location = f"static/images/{image.filename}"
        async with aiofiles.open(file_location, 'wb') as f:
            await f.write(contents)

        return file_location
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Файл изображения не корректен, загрузите другое '
                   'изображение'
        )


async def check_author_exists(
        author_id: int,
        session: AsyncSession,
) -> Author:
    """Проверка, что автор с переданным id существует."""
    author = await author_crud.get(author_id, session)
    if author is None:
        raise HTTPException(
            status_code=404,
            detail='Автор не найден!'
        )
    return author


async def check_book_exists(
        book_id: int,
        session: AsyncSession,
) -> Book:
    """Проверка, что книга с переданным id существует."""
    book = await book_crud.get(book_id, session)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail='Книга не найден!'
        )
    return book


async def check_genre_exists(
        genre_id: int,
        session: AsyncSession,
) -> Genre:
    """Проверка, что жанр с переданным id существует."""
    genre = await genre_crud.get(genre_id, session)
    if genre is None:
        raise HTTPException(
            status_code=404,
            detail='Жанр не найден!'
        )
    return genre


async def check_all_genre_exists(
        genre_ids: list[int],
        session: AsyncSession,
) -> list[Genre]:
    """Проверка, что жанры с переданным списком id существуют."""
    genres = await genre_crud.get_genres_by_list_ids(
        genre_ids=genre_ids,
        session=session
    )
    if len(genres) != len(genre_ids):
        raise HTTPException(
            status_code=400,
            detail="Передан невалидный список жанров"
        )
    return genres


async def check_genre_name_duplicate(
        genre_name: str,
        session: AsyncSession,
) -> None:
    """Проверка дубликатов названия жанров."""
    genre_id = await genre_crud.get_genre_id_by_name(genre_name, session)
    if genre_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Жанр с таким именем уже существует!',
        )


async def check_reservation_intersections(**kwargs) -> None:
    """Проверка пересечений бронирований."""
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )


async def check_reservation_before_edit(
        reservation_id: int,
        session: AsyncSession,
        user: User
) -> Reservation:
    """Проверка существования и возможности редактирования бронирования """
    reservation = await reservation_crud.get(
        obj_id=reservation_id, session=session
    )
    if not reservation:
        raise HTTPException(status_code=404, detail='Бронь не найдена!')
    if not (reservation.user_id == user.id or user.is_superuser):
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую бронь!'
        )
    return reservation
