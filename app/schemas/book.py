from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    """Базовая схема автора."""

    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=0)
    pages: int = Field(..., gt=0)
    author_id: int
    genre_id: int


class BookCreate(BookBase):
    """Создания книги."""


class BookDB(BookBase):
    """Получение информации о книге."""

    id: int
    model_config = ConfigDict(from_attributes=True)
