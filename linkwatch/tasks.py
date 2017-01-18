from celery import Celery
from celery.utils.log import get_task_logger

from kombu import Queue, Exchange
from kombu.common import Broadcast

import endpoints
import sys

from custom_logging import logger
from settings import *

app = Celery('api.tasks', broker=BROKER_URL)
app.conf.update(
    CELERY_DEFAULT_QUEUE=BROKER_QUEUE,
    CELERY_QUEUES=(
        Broadcast(BROKER_QUEUE),
    ),
)

@app.task(name=BROKER_TASK)
def parse_measurement(measurement_json):
    logger.debug('[linkwatch] Parse measurement request: %s' % (measurement_json))
    endpoints.save_measurement(measurement_json)