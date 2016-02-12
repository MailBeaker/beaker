
from celery import Celery

from settings import CELERY_AWS_BROKER_URL


def get_celery_app():

    app = Celery(
        broker=CELERY_AWS_BROKER_URL
    )

    return app
