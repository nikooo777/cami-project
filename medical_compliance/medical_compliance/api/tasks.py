"""
Define tasks that can be sent by other services through the RabbitMQ broker.
All tasks have manually defined names instead of automatic[1] to eliminate the
need to have the same module structure in the worker and the client.
[1] http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-naming-relative-imports
"""

import json
import datetime

from celery import Celery
from celery.utils.log import get_task_logger
from kombu import Queue, Exchange
from django.conf import settings #noqa

import google_fit

from models import WeightMeasurement, HeartRateMeasurement

from analyzers.weight_analyzers import analyze_weights
from analyzers.heart_rate_analyzers import analyze_heart_rates

logger = get_task_logger('medical_compliance_measurements.fetch_measurement')

global_app = Celery()
global_app.config_from_object('django.conf:settings')

app = Celery('api.tasks', broker=settings.BROKER_URL)
app.conf.update(
    CELERY_DEFAULT_QUEUE='medical_compliance_measurements',
    CELERY_QUEUES=(
        Queue('medical_compliance_measurements', Exchange('medical_compliance_measurements'), routing_key='medical_compliance_measurements'),
    ),
)


@app.task(name='medical_compliance_measurements.process_weight_measurement')
def process_weight_measurement(user_id, input_source, measurement_unit, timestamp, timezone, value):
    logger.debug("[medical-compliance] Fetch weight measurement request: %s" % (locals()))

    weight_measurement = WeightMeasurement(
        user_id = int(user_id),
        input_source=input_source,
        measurement_unit=measurement_unit,
        timestamp=timestamp,
        timezone=timezone,
        value=value
    )

    logger.debug("[medical-compliance] Saving weight measurement: %s" % (weight_measurement))
    weight_measurement.save()

    logger.debug("[medical-compliance] Sending the weight measurement with id %s for analysis." % (weight_measurement.id))
    analyze_weights.delay(weight_measurement.id)

    logger.debug("[medical-compliance] Broadcasting weight measurement: %s" % (weight_measurement))
    broadcast_measurement('weight', weight_measurement)

@app.task(name='medical_compliance_measurements.process_heart_rate_measurement')
def process_heart_rate_measurement():
    """
        It's very ugly what I did here, only for demo purpose
        We MUST clean this
    """
    logger.debug("[medical-compliance] Fetch heart measurement request: %s. Retrieving test and cinch heart rate measurements since the last one..." % (locals()))

    last_cinch_measurement = None
    last_test_measurement = None
    
    try:
        last_cinch_measurement = HeartRateMeasurement.objects.all().filter(input_source='cinch').order_by('-timestamp')[0]
        time_from_cinch = last_cinch_measurement.timestamp + 1
    except:
        time_from_cinch = 0

    try:
        last_test_measurement = HeartRateMeasurement.objects.all().filter(input_source='test').order_by('-timestamp')[0]
        time_from_test = last_test_measurement.timestamp + 1
    except:
        time_from_test = 0

    time_to = int(
        (
            datetime.datetime.today() + 
            datetime.timedelta(days=30) - 
            datetime.datetime(1970, 1, 1)
        ).total_seconds()
    )
    
    measurements = google_fit.get_heart_rate_data_from_cinch(time_from_cinch, time_to)
    measurements = measurements + google_fit.get_heart_rate_data_from_test(time_from_test, time_to)
    
    for m in measurements:
        heart_rate_measurement = HeartRateMeasurement(
            user_id = 11262861,
            input_source=m['source'],
            measurement_unit='bpm',
            timestamp=m['timestamp'],
            timezone='Europe/Bucharest',
            value=m['value']
        )

        logger.debug("[medical-compliance] Saving heart rate measurement: %s" % (heart_rate_measurement))
        heart_rate_measurement.save()

        logger.debug("[medical-compliance] Broadcasting heart rate measurement: %s" % (heart_rate_measurement))
        broadcast_measurement('heartrate', heart_rate_measurement)
    
    logger.debug("[medical-compliance] Sending the last cinch heart rate measurement for analysis: %s" % (last_cinch_measurement))
    analyze_heart_rates.delay(last_cinch_measurement, 'cinch')

    logger.debug("[medical-compliance] Sending the last test heart rate measurement for analysis: %s" % (last_test_measurement))
    analyze_heart_rates.delay(last_test_measurement, 'test')

    return json.dumps(measurements, indent=4, sort_keys=True)


def broadcast_measurement(measurement_type, measurement):
    measurement_json = {
        'type': measurement_type,
        'user_id': measurement.user_id,
        'input_source': measurement.input_source,
        'measurement_unit': measurement.measurement_unit,
        'timestamp': measurement.timestamp,
        'timezone': measurement.timezone,
        'value': measurement.value
    }
    
    global_app.send_task('cami.on_measurement_received', [measurement_json], queue='broadcast_measurement')
    