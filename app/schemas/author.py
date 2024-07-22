from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class AuthorBase(BaseModel):
    """Базовая схема автора."""

    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)


class AuthorCreate(AuthorBase):
    """Схема для создания автора."""

    avatar: str
    pass


class AuthorDB(AuthorBase):
    """Получение информации об авторе."""

    id: int
    avatar: str
    model_config = ConfigDict(from_attributes=True)
