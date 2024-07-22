import aiofiles
from fastapi import HTTPException, UploadFile


async def validate_image(
        image: UploadFile,
):
    try:
        file_location = f"static/images/{image.filename}"
        async with aiofiles.open(file_location, 'wb') as f:
            while content := await image.read():
                await f.write(content)
                return file_location
    except Exception:
        raise HTTPException(
            status_code=400,
            detail='Файл изображения не корректен, загрузите другое '
                   'изображение'
        )
