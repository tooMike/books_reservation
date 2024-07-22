from io import BytesIO

import aiofiles
from fastapi import HTTPException, UploadFile
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.author import author_crud
from app.models.author import Author


async def validate_image(image: UploadFile) -> str:
    """Валидация изображения."""
    try:
        contents = await image.read()

        try:
            Image.open(BytesIO(contents)).verify()
        except (IOError, SyntaxError):
            raise HTTPException(
                status_code=400,
                detail='Файл изображения не корректен, загрузите другое '
                       'изображение'
            )

        # Запишем файл на диск
        file_location = f"static/images/{image.filename}"
        async with aiofiles.open(file_location, 'wb') as f:
            await f.write(contents)

        return file_location
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Файл изображения не корректен, загрузите другое '
                   'изображение'
        )

async def check_author_exists(
    author_id: int,
    session: AsyncSession,
) -> Author:
    author = await author_crud.get(author_id, session)
    if author is None:
        raise HTTPException(
            status_code=404,
            detail='Автор не найден!'
        )
    return author
