from decouple import config 

from settings.base import * #noqa 


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("MOVIENIGHT_POSTQGRES_DB", cast=str),
        'USER': config("MOVIENIGHT_POSTQGRES_USER", cast=str),
        'PASSWORD': config("MOVIENIGHT_POSTQGRES_PASSWORD", cast=str),
        'HOST': config("MOVIENIGHT_POSTQGRES_HOST", cast=str),
        'PORT': config("MOVIENIGHT_POSTQGRES_PORT", cast=str),
    }
}