from fastapi import APIRouter

from app.api.endpoints import (
    author_router,
    book_router,
    genre_router,
    reservation_router,
    users_router,
)

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(author_router, prefix='/author', tags=['Author'])
main_router.include_router(book_router, prefix='/book', tags=['Book'])
main_router.include_router(genre_router, prefix='/genre', tags=['Genre'])
main_router.include_router(
    reservation_router,
    prefix='/reservation',
    tags=['Reservation']
)
