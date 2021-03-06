# Create your views here.

import json, logging, pprint
import store_utils

from django.http import HttpResponse, HttpRequest, HttpResponseServerError
from django.conf import settings #noqa
from django.views.decorators.csrf import csrf_exempt

from withings import WithingsApi, WithingsCredentials
from withings_tasks import retrieve_and_save_withings_measurements
from tasks import process_heart_rate_measurement

from withings_utils import get_withings_user
import store_utils

logger = logging.getLogger("medical_compliance.measurement_callback")

def get_full_callback_url(request):
    ## For now, it remains hardcoded that the weight measurements are taken using the Withings WS 30 weight scale
    ## TODO: figure out a way to get hold of the corresponding device data automatically

    # hostname = request.META['SERVER_NAME']
    # port = request.META['SERVER_PORT']
    endpoint_host_uri = "http://" + store_utils.STORE_HOST + ":" + store_utils.STORE_PORT

    device_data = store_utils.get_device(endpoint_host_uri, manufacturer ="Withings", model ="WS 30")
    device_id = device_data['id']

    withings_measurement_notification_path = "/measurements_notification" + "/" + str(device_id) + "/"
    return request.build_absolute_uri(withings_measurement_notification_path)


def subscribe_notifications(request):
    logger.debug("[medical-compliance] Notifications subscribe was called.")

    withings_user = None
    try:
        withings_user = get_withings_user(settings.WITHINGS_USER_ID)
    except Exception as e:
        logger.error("[medical-compliance] Unable to retrieve withings user by userid in the settings file: %s" % (e))
        return HttpResponseServerError("User with id %s could not be found." % (settings.WITHINGS_USER_ID))

    credentials = WithingsCredentials(access_token=withings_user.oauth_token,
                                      access_token_secret=withings_user.oauth_token_secret,
                                      consumer_key=settings.WITHINGS_CONSUMER_KEY,
                                      consumer_secret=settings.WITHINGS_CONSUMER_SECRET,
                                      user_id=withings_user.userid)
    client = WithingsApi(credentials)

    callback_uri = get_full_callback_url(request)
    logger.debug("[medical-compliance] Subscribing to Withings notifications for user_id=%s with URI: %s." % (
        withings_user.userid, callback_uri))

    response_data = client.subscribe(callback_uri, "Subscribe for weight measurement notifications.", appli=1)
    logger.debug("[medical-compliance] Notifications subscribe response: %s." % (response_data))

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def unsubscribe_notifications(request):
    logger.debug("[medical-compliance] Notifications unsubscribe was called.")

    withings_user = None
    try:
        withings_user = get_withings_user(settings.WITHINGS_USER_ID)
    except Exception as e:
        logger.error("[medical-compliance] Unable to retrieve withings user by userid in the settings file: %s" % (e))
        return HttpResponseServerError("User with id %s could not be found." % (settings.WITHINGS_USER_ID))

    credentials = WithingsCredentials(access_token=withings_user.oauth_token,
                                      access_token_secret=withings_user.oauth_token_secret,
                                      consumer_key=settings.WITHINGS_CONSUMER_KEY,
                                      consumer_secret=settings.WITHINGS_CONSUMER_SECRET,
                                      user_id=withings_user.userid)
    client = WithingsApi(credentials)
    response_data = client.unsubscribe(get_full_callback_url(request), appli=1)    
    logger.debug("[medical-compliance] Notifications unsubscribe response: %s." % (response_data))

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def test_heart_rate_fetch(request):
    return HttpResponse(process_heart_rate_measurement(), content_type="text/html")

@csrf_exempt
def measurements_notification_received(request, device_id):
    logger.debug("[medical-compliance] Measurements hook was called: %s" % (request.POST))

    #device_id = store_utils.get_id_from_uri_path(request.path)

    if request.POST.has_key("userid"):
        withings_userid = request.POST['userid']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        appli = request.POST['appli']

        logger.debug("[medical-compliance] Passing data to the retrieve_and_save_withings_measurements task: { withings_userid: %s, device_id: %s, startdate: %s, enddate: %s, appli: %s }" %
            (withings_userid, device_id, startdate, enddate, appli))
        retrieve_and_save_withings_measurements.delay(withings_userid, device_id, startdate, enddate, appli)
    else:
        logger.debug("[medical-compliance] Received invalid POST data in measurements hook - possibly related to a subscribe call")

    return HttpResponse(status=200)