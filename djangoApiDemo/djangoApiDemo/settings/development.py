from djangoApiDemo.settings.base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY', 'default-django-secret-key')

DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': config('DB_NAME'),
    #     'USER': config('MySQL_USER', default='root'),
    #     'PASSWORD': config('MySQL_PASSWORD', default='root'),
    #     'HOST': config('DB_HOST', default='localhost'),
    #     'PORT': config('DB_PORT', default='3306'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
