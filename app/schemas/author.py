from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    """Базовая схема автора."""

    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    avatar: str


class AuthorCreate(AuthorBase):
    """Создания автора."""


class AuthorDB(AuthorBase):
    """Получение информации об авторе."""

    id: int
    model_config = ConfigDict(from_attributes=True)
