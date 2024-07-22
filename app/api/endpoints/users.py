from fastapi import APIRouter, Depends, UploadFile

from app.api.validators import validate_image
from app.core.users import (
    auth_backend,
    current_user,
    fastapi_users,
    get_user_manager, UserManager,
)
from app.models import User
from app.schemas.users import UserCreate, UserRead, UserReadDB

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


@router.post('/upload_avatar', response_model=UserReadDB)
async def create_avatar(
        avatar: UploadFile,
        user: User = Depends(current_user),
        user_manager: UserManager = Depends(get_user_manager)
):
    image_path = await validate_image(image=avatar)
    user = await user_manager.create_avatar(user=user, avatar=image_path)
    return user
