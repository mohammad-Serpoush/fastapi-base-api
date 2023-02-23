from celery import Celery
from app.core.config import settings

# from app.core.postman.tasks import campaign_terminal

celery = Celery(__name__, include=["app.core.tasks", "app.core.tasks"])

celery.conf.broker_url = settings.CELERY_URI
celery.conf.result_backend = settings.CELERY_URI
