from celery import Celery

from app.core.config import settings


celery = Celery(
    "tasks",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}",
    include=["app.tasks.tasks"]
)
