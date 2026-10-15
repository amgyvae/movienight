from settings.base import * # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}