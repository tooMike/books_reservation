from pydantic import BaseModel, ConfigDict, Field

from app.schemas.genre import GenreDB


class BookBase(BaseModel):
    """Базовая схема автора."""

    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=0)
    pages: int = Field(..., gt=0)
    author_id: int
    genres: list[int]


class BookCreate(BookBase):
    """Создания книги."""


class BookUpdate(BaseModel):
    """Изменение книги."""

    name: str | None = Field(None, min_length=3)
    price: float | None = Field(None, ge=0)
    pages: int | None = Field(None, gt=0)
    author_id: int | None = None
    genres: list[int] | None = None


class BookDB(BookBase):
    """Получение информации о книге."""

    id: int
    genres: list[GenreDB]
    model_config = ConfigDict(from_attributes=True)


class BookFilter(BaseModel):
    """Фильтрация книг по цене, авторам и жанрам."""

    author_ids: list[int] | None = None
    genre_ids: list[int] | None = None
    min_price: float | None = Field(None, ge=0)
    max_price: float | None = Field(None, ge=0)
