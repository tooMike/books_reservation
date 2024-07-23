Запуск Celery

# Запуск Celery Worker
celery -A app.celery_worker worker --loglevel=info

# Запуск Celery Beat в отдельном терминале
celery -A app.celery_worker beat --loglevel=info


Загрузка тестовый данных




Установка

 docker compose exec web bash

Выполнение миграций


 alembic upgrade head


Загрузка тестовых данных:
python -m app.test_data.add_data


Проект будет доступен по адресу: 
http://127.0.0.1:8000/docs