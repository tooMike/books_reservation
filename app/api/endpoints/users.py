from fastapi import APIRouter

from app.core.users import (
    auth_backend,
    fastapi_users,
)
from app.schemas.users import UserCreate, UserRead

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Users'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Users'],
)
