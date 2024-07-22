from fastapi import APIRouter

from app.api.endpoints import users_router, author_router
main_router = APIRouter()

main_router.include_router(users_router, prefix='/users', tags=['Users'])
main_router.include_router(author_router, prefix='/author', tags=['Author'])



