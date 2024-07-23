from datetime import datetime, timedelta

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)

FROM_TIME = (
        datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
        datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(
        ...,
        example=FROM_TIME
    )
    to_reserve: datetime = Field(
        ...,
        example=TO_TIME
    )

    model_config = {'extra': 'forbid'}


class ReservationUpdate(ReservationBase):
    """Схема для обновления бронирования."""

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(
            cls,
            from_reserve: datetime
    ) -> datetime:
        if from_reserve <= datetime.now():
            raise ValueError("Нельзя забронировать время в прошлом")
        return from_reserve

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self):
        if self.to_reserve <= self.from_reserve:
            raise ValueError(
                "Дата окончания бронирования не может быть раньше начала"
            )
        return self


class ReservationCreate(ReservationBase):
    """Схема бронирования книги."""

    book_id: int


class ReservationDB(ReservationBase):
    """Схема для отображения бронирования."""

    id: int
    book_id: int
    user_id: int | None

    model_config = ConfigDict(from_attributes=True)
