from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    """Базовая схема автора."""

    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    avatar: str


class AuthorCreate(AuthorBase):
    """Создания автора."""


class AuthorUpdate(AuthorBase):
    """Обновление автора."""

    first_name: str | None = Field(None, min_length=3)
    last_name: str | None = Field(None, min_length=3)
    avatar: str | None = None


class AuthorDB(AuthorBase):
    """Получение информации об авторе."""

    id: int
    model_config = ConfigDict(from_attributes=True)
