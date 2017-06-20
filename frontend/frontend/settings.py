"""
Django settings for frontend project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import raven

from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mt&sg^ly330k6r8*t2mo_&!-8stx5f7fn=q1f2nn4=jcslb7si'

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

ROOT_URLCONF = 'frontend.urls'

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

WSGI_APPLICATION = 'frontend.wsgi.application'

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
        'syslog': {
            'level':'DEBUG',
            'class':'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address':(PAPERTRAILS_LOGGING_HOSTNAME, PAPERTRAILS_LOGGING_PORT)
        },
    },
    'loggers': {
        'frontend': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'syslog'],
        },
        'api': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'syslog'],
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console'],
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
        'frontend.tasks': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console', 'syslog'],
        },
    },
}

SENTRY_AUTO_LOG_STACKS = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# Options from here: https://blog.ionelmc.ro/2014/12/28/terrible-choices-mysql/
DATABASES = {}

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
TASTYPIE_DATETIME_FORMATTING = 'iso-8601-strict'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS='ALLOW-FROM *'

# Celery settings
BROKER_URL = 'amqp://cami:cami@cami-rabbitmq:5672/cami'

CELERY_DEFAULT_QUEUE = 'frontend_notifications'
CELERY_QUEUES = (
    Queue('frontend_notifications', Exchange('frontend_notifications'), routing_key='frontend_notifications'),
)

# Healthchecker settings
RABBITMQ_CHECK_TIMEOUT = 1

PUSH_NOTIFICATIONS_SETTINGS = {
    "APNS_CERTIFICATE": "/cami-project/frontend/frontend/push-notifications/ios/prod/apns-cert.pem"
}

try:
    from settings_local import *
except:
    pass
