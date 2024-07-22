from pydantic import BaseModel, ConfigDict, Field


class GenreBase(BaseModel):
    """Базовая схема жанра."""

    name: str = Field(..., min_length=3)


class GenreCreate(GenreBase):
    """Создания жанра."""


class GenreDB(GenreBase):
    """Получение информации о жанре."""

    id: int
    model_config = ConfigDict(from_attributes=True)
