from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.author import Author


class CRUDAuthor(CRUDBase):

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """Изменение автора."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        # Удаление ключей с None значениями
        update_data = {k: v for k, v in update_data.items() if v is not None}

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


author_crud = CRUDAuthor(Author)
