from pydantic import BaseModel, ConfigDict, Field

from app.models import Genre
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




class BookDB(BaseModel):
    """Получение информации о книге."""

    id: int
    name: str
    price: float
    pages: int
    author_id: int
    genres: list[GenreDB]
    model_config = ConfigDict(from_attributes=True)
