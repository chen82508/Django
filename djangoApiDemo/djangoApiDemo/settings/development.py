from djangoApiDemo.settings.base import *

SECRET_KEY = config('SECRET_KEY', 'default-django-secret-key')

DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('MySQL_USER', default='root'),
        'PASSWORD': config('MySQL_PASSWORD', default='root'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

INSTALLED_APPS += [
    'authentication',
]

AUTH_USER_MODEL = 'authentication.User'