from celery import Celery
from src.core.config import Settings

settings = Settings()

celery = Celery(
    "worker",
    broker=settings.REDIS_URL.unicode_string(),
    backend=settings.REDIS_URL.unicode_string()
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery.autodiscover_tasks(["src.worker"])