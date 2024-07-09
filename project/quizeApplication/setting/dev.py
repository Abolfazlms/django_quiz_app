
from quizeApplication.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(0%m(^nwm7zk=mlv&yckopkpq1-!pe*qh_&1fi*ix8m)xrjjor'
DEBUG = True
ALLOWED_HOSTS = ['heyweb.ir','www.heyweb.ir','127.0.0.1']

# INSTALLED_APPS = [
# ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / 'statics',
]
