import asyncio

from ..core.db import AsyncSessionLocal
from ..models import Author, Book, Genre

# Создание тестовых данных
# Авторы
author1 = Author(
    first_name="Иван",
    last_name="Иванов",
    avatar="link_to_avatar1"
)
author2 = Author(
    first_name="Петр",
    last_name="Петров",
    avatar="link_to_avatar2"
)

# Жанры
genre1 = Genre(name="Фантастика")
genre2 = Genre(name="Классика")

# Книги
book1 = Book(
    name="Книга 1",
    price=450.50,
    pages=300,
    author=author1,
    genres=[genre1, genre2]
)
book2 = Book(
    name="Книга 2",
    price=550.00,
    pages=200,
    author=author1,
    genres=[genre1]
)


async def add_test_data():
    async with AsyncSessionLocal() as async_session:
        try:
            async_session.add_all(
                [author1, author2, genre1, genre2, book1, book2]
            )
            await async_session.commit()
        finally:
            await async_session.close()


if __name__ == '__main__':
    asyncio.run(add_test_data())
