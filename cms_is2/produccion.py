from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['cms.local', 'localhost','0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cms_prod',
        'USER': 'cmsadmin',
        'PASSWORD': 'cmsadmin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}