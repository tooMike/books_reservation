from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_author_exists, validate_image
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.author import author_crud
from app.schemas.author import AuthorCreate, AuthorDB

router = APIRouter()


@router.post(
    '/',
    response_model=AuthorDB,
    # dependencies=[Depends(current_superuser)]
)
async def create_author(
        first_name: str,
        last_name: str,
        avatar: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session)
):
    image_path = await validate_image(image=avatar)
    obj_in = AuthorCreate(
        first_name=first_name,
        last_name=last_name,
        avatar=image_path
    )
    author = await author_crud.create(
        obj_in=obj_in,
        session=session,
    )
    return author


@router.delete(
    '/{author_id}',
    response_model=AuthorDB,
    # dependencies=[Depends(current_superuser)]
)
async def delete_author(
        author_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление автора."""
    author = await check_author_exists(author_id=author_id, session=session)
    author = await author_crud.remove(author_id=author_id, session=session)
    return author
