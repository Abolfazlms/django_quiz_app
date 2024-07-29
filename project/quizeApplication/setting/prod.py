from quizeApplication.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(0%m(^nwm7zk=mlv&yckopkpq1-!pe*qh_&1fi*ix8m)xrjjor'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['heyweb.ir','www.heyweb.ir','127.0.0.1']
# INSTALLED_APPS = [
# ]
AUTH_USER_MODEL = 'account.CustomUser'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# STATIC_ROOT = '/home/heywebir/public_html/static'
# MEDIA_ROOT = '/home/heywebir/public_html/media'


STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'


STATICFILES_DIRS = [
    BASE_DIR / 'statics',
]

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['http://www.heyweb.ir']