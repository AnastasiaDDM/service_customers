'''Настройки для проекта serviceCustomers.'''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', default='*').split(' ')


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'customers',
    'service',
    'favorites',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'servicecustomers.urls'


WSGI_APPLICATION = 'servicecustomers.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD']

    },
    'mssql_db': {
        'ENGINE': 'mssql',
        'HOST': os.environ['MSSQL_HOST'],
        'PORT': os.environ['MSSQL_PORT'],
        'NAME': os.environ['MSSQL_DB'],
        'USER': os.environ['MSSQL_USER'],
        'PASSWORD': os.environ['MSSQL_PASSWORD'],
        'TIME_ZONE': 'Asia/Irkutsk',
        'OPTIONS': {
            'connection_timeout': int(os.environ['MSSQL_TIMEOUT']),
            'connection_retries': int(os.environ['MSSQL_RETRIES_COUNT']),
            'connection_retry_backoff_time': int(os.environ['MSSQL_RETRIES_SLEEP']),
            'driver': 'ODBC Driver 18 for SQL Server',
            'unicode_results': True,
            'extra_params': 'Encrypt=no',
        }

    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {

    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },

    # Для тестирования (логирование запросов в бд)
    "loggers": {
        'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
    }
}