from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(schemas.CreateUpdateDictModel):
    """Базовая схема пользователя."""

    name: str
    surname: str
    email: EmailStr


class UserRead(UserBase):
    """Получение информации о пользователе."""
    avatar: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Создание пользователя."""

    password: str


class UserUpdate(schemas.BaseUserUpdate):
    """Изменение информации о пользователе."""

    name: str | None = None
    surname: str | None = None


class UserAvatarCreate(BaseModel):
    """Добавление аватара"""

    avatar: str

    @field_validator('avatar')
    @classmethod
    def validate_avatar(cls, value: str) -> str:
        """Проверяем, что аватар передан в правильном формате Base64."""
        if value:
            parts = value.split(',')
            if len(parts) != 2:
                raise ValueError(
                    'Невалидный формат изображения'
                )

            header, encoded = parts
            if not header.startswith('data:image'):
                raise ValueError(
                    'Невалидный формат изображения. Начало должно быть – '
                    'data:image'
                )

            # Проверка допустимого типа MIME
            allowed_types = ['jpeg', 'png', 'gif']
            if not any(f'image/{mime}' in header for mime in allowed_types):
                raise ValueError(
                    f'Невалидный формат изображения: разрешенные форматы: '
                    f'{allowed_types}'
                )

        return value
