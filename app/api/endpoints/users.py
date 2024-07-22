from fastapi import APIRouter, Depends, UploadFile

from app.api.validators import validate_image
from app.core.users import (
    auth_backend,
    current_user,
    fastapi_users,
    get_user_manager, UserManager,
)
from app.models import User
from app.schemas.users import UserCreate, UserRead

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


@router.post('/avatar', response_model=UserRead)
async def create_avatar(
        avatar: UploadFile,
        user: User = Depends(current_user),
        user_manager: UserManager = Depends(get_user_manager)
):
    image_path = await validate_image(image=avatar)
    user = await user_manager.create_avatar(user=user, avatar=image_path)
    return user


@router.delete(
    '/avatar',
    response_model=UserRead,
    response_model_exclude_none=True
)
async def delete_avatar(
        user: User = Depends(current_user),
        user_manager: UserManager = Depends(get_user_manager)
):
    user = await user_manager.delete_avatar(user=user)
    return user
