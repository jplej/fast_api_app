from celery import Celery

celery_client = Celery(
    "fastapi_client",
    broker="redis://redis:6379/0",  # Use Redis as a broker
    backend="redis://redis:6379/0"  # Redis result backend
)
