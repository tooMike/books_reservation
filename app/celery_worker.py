from celery import Celery
from celery.schedules import crontab

# Конфигурация Celery
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Планировщик Celery Beat для ежедневного выполнения задачи
app.conf.beat_schedule = {
    'remove_expired_reservations_daily': {
        'task': 'app.tasks.remove_expired_reservations',
        'schedule': crontab(minute=0, hour=0)  # Запуск в полночь каждый день
    },
}

app.autodiscover_tasks()
