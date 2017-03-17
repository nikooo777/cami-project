"""
Django settings for medical_compliance project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import raven

from datetime import timedelta
from kombu import Exchange, Queue
from kombu.common import Broadcast

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(zawb(0eluv_yf-*r@_zpl--#3^5wgg2w)g83xd&1#59g)7&!b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'corsheaders',
    'tastypie',
    'medical_compliance.api',
    'medical_compliance.api.analyzers'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medical_compliance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'medical_compliance.wsgi.application'

# Sentry integration
RAVEN_CONFIG = {
    # Set the Sentry API key here
    'dsn': 'https://d9bec7e9f54943a281d5271c29932e7c:b57cfbbc5edc456aa2ece299cabbd785@sentry.io/104123',
    'release': raven.fetch_git_sha(os.path.dirname(__file__) + "/../../")
}

PAPERTRAILS_LOGGING_HOSTNAME = 'logs4.papertrailapp.com'
PAPERTRAILS_LOGGING_PORT = 43843
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # Set the Sentry logging level here
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
        'syslog': {
            'level':'DEBUG',
            'class':'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address':(PAPERTRAILS_LOGGING_HOSTNAME, PAPERTRAILS_LOGGING_PORT)
        },
    },
    'loggers': {
        'medical_compliance': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'syslog'],
        },
        'api': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'syslog'],
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'file'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'level': 'ERROR',
            'handlers': ['sentry', 'console'],
        },
        'medical_compliance.measurement_callback': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'withings_controller.retrieve_and_save_withings_measurements': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'medical_compliance_measurements.process_measurement': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'medical_compliance_heart_rate_analyzers.analyze_heart_rates': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'medical_compliance_weight_analyzers.analyze_weight': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'medical_compliance.google_fit': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'medical_compliance.store_utils': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

SENTRY_AUTO_LOG_STACKS = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cami',
        'USER': 'cami',
        'PASSWORD': 'cami',
        'HOST': 'cami-store',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TASTYPIE_DEFAULT_FORMATS = ['json']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS='ALLOW-FROM *'


# WITHINGS API credentials
# WITHINGS_USER_ID = 11262861
# WITHINGS_CONSUMER_KEY = "734b6504c858bed3e3ecd7ce78b543f5f9e3cbe9b1b41fc40f012d1fdc96"
# WITHINGS_CONSUMER_SECRET = "4f3d74e3f148781ee6459cc881186b24e2c3850530b6370e60d81b5822"

# WITHINGS_OAUTH_V1_TOKEN = "394b9199422126c1ffc405bf003dd26cc6259cd02c8dee230b8bcd12634de5"
# WITHINGS_OAUTH_V1_TOKEN_SECRET = "5643779f862c5030c5631fd3387233cbf8465b8520c5b4b073850fd"

# Temporary WITHINGS API credentials for the demo
WITHINGS_CONSUMER_KEY = "5b1f8cbeb36cffe108fd8fdd666c51cb5d6eee9f2e2940983958b836451"
WITHINGS_CONSUMER_SECRET = "2e75dfb7f1088f398b4cfc5ebed6d5909c48918ee637417e3b0de001b3b"
WITHINGS_USER_ID = 11115034

WITHINGS_USERS = [
    {
        "userid": 11115034,
        "oauth_token": "59dd58ccbd19bfbd8b3522ce50d31c4cb6e530742d22234f4cb4bee11673084",
        "oauth_token_secret": "cf31bc8e405d96b975b8014d93c722830bd55f44b437f27c7e6d5964b3"
    },
]

# Google Fit API credentials
GOOGLE_FIT_CLIENT_ID = '701996606933-17j7km8f8ce8vohhdcnur453cbn44aau.apps.googleusercontent.com'
GOOGLE_FIT_CLIENT_SECRET = 'K-lZ7t49-Gvhtz2P-RTqBhAQ'
GOOGLE_FIT_REFRESH_TOKEN = '1/eAhtNXxq65LeyzTr4aju27wCPLDAipXdrEd8ovgO8CY'

# Google Fit data streams
GOOGLE_FIT_HR_TEST_DATASTREAM_NAME = 'CAMI Heart Rate Test'
GOOGLE_FIT_HR_DATASTREAM_ID = 'raw:com.google.heart_rate.bpm:com.ryansteckler.perfectcinch:'

GOOGLE_FIT_STEPS_TEST_DATASTREAM_NAME = 'CAMI Steps Test'

# Google Fit Fetch Heart Rate Scheduled Task
CELERYBEAT_SCHEDULE = {
    'fetch_heart_rate_data': {
        'task': 'medical_compliance_measurements.process_heart_rate_measurement',
        'schedule': timedelta(minutes=5),
    },
    'fetch_steps_data': {
        'task': 'medical_compliance_measurements.process_steps_measurement',
        'schedule': timedelta(minutes=5),
    }
}

# Celery settings
BROKER_URL = 'amqp://cami:cami@cami-rabbitmq:5672/cami'

CELERY_DEFAULT_QUEUE = 'withings_measurements'
CELERY_QUEUES = (
    Queue('withings_measurements', Exchange('withings_measurements'), routing_key='withings_measurements'),
    Queue('medical_compliance_measurements', Exchange('medical_compliance_measurements'), routing_key='medical_compliance_measurements'),
    Queue('medical_compliance_weight_analyzers', Exchange('medical_compliance_weight_analyzers'), routing_key='medical_compliance_weight_analyzers'),
    Queue('medical_compliance_heart_rate_analyzers', Exchange('medical_compliance_heart_rate_analyzers'), routing_key='medical_compliance_heart_rate_analyzers'),
    Broadcast('broadcast_measurement'),
)
# Every measurement sent on the broadcast_measurement queue will be broadcasted to all the workers that listen on the cami.on_measurement_received task on it
CELERY_ROUTES = {'cami.on_measurement_received': {'queue': 'broadcast_measurement'}}

try:
    from settings_local import *
except:
    pass
