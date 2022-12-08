"""
Django settings for muya_wce project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
from pathlib import Path

import logging

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def resolve_callable(val):
    return val() if callable(val) else val


# Environment variables that affect settings values
env = environ.Env(
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
    DEBUG=(bool, False),
    LOG_LEVEL_DJANGO=(str, 'INFO'),
    LOG_LEVEL=(resolve_callable, lambda: ('DEBUG' if DEBUG else 'INFO')),
    PUBLIC_URL=str,
    STATIC_URL=(str, '/static/'),
    LOGIN_URL=(str, '/accounts/login/'),
    SECRET_KEY=str,
    COLLATEX_URL=str,
    CELERY_BROKER_URL=str,
    CELERY_RESULT_BACKEND=str,
    EMAIL_BACKEND=(str, 'django.core.mail.backends.filebased.EmailBackend'),
    EMAIL_FILE_PATH=(str, str(BASE_DIR / 'sent_emails')),
    EMAIL_HOST=(str, 'localhost'),
    EMAIL_PORT=(str, 587),
    EMAIL_USE_TLS=(bool, True),
    DEFAULT_FROM_EMAIL=str,
    CONTACT_EMAIL=str,
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
    USER_IDENTIFIER_FIELD=(str, 'full_name'),
)

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

# CollateX API setup
COLLATEX_URL = env('COLLATEX_URL')

# Celery setup
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_RESULT_EXTENDED = True


# Detect whether we're running under WSGI (i.e. as a webserver)
WSGI = 'django.core.wsgi' in sys.modules
WSGI_APPLICATION = 'muya_wce.wsgi.application'

DATABASES = {
    'default': env.db_url('DATABASE_URL', engine='postgresql')
}

# Override database config to enforce some required options
DATABASES['default']['CONN_MAX_AGE'] = 10
DATABASES['default']['OPTIONS'] = {
    **DATABASES['default'].get('OPTIONS', {}),
    **{'application_name': 'Django - MUYA WCE'}
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'muya_wce.setup.apps.SetupConfig',
    'accounts.apps.AccountsConfig',
    'transcriptions.apps.TranscriptionsConfig',
    'collation.apps.CollationConfig',
    'rest_framework',
    'api.apps.ApiConfig',
]


if 'test' in sys.argv:
    TESTING = True
else:
    TESTING = False

# This app is only used for testing and should not be installed in production
# Run the tests with `python manage.py test api_tests`
# @TODO There may be a better way to handle this?
if TESTING:
    INSTALLED_APPS.append('api_tests.apps.ApitestsConfig')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'muya_wce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'muya_wce' / 'templates'],
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

# User and login setup
LOGIN_URL = env('LOGIN_URL')
AUTH_USER_MODEL = 'accounts.User'
USER_IDENTIFIER_FIELD = env('USER_IDENTIFIER_FIELD')

# django-rest-framework settings
REST_FRAMEWORK = {'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
                  'PAGE_SIZE': 100,
                  'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
                   ],
                  'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',)
                  }


EMAIL_BACKEND = env('EMAIL_BACKEND')
# Production
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
CONTACT_EMAIL = env('CONTACT_EMAIL')

# Local development only. Not for use in Production.
# https://docs.djangoproject.com/en/3.2/topics/email/#file-backend
EMAIL_FILE_PATH = env('EMAIL_FILE_PATH')

# Export directories
# NB: These will not persist in a containerized environment
APPARATUS_BASE_DIR = BASE_DIR / 'apparatus'
EXPORT_BASE_DIR = BASE_DIR / 'exports'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
if not DEBUG:
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Hardening for websites
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = env('STATIC_URL')
STATIC_ROOT = str(BASE_DIR / 'static')
STATICFILES_DIRS = [
                    ('common', BASE_DIR / 'common-static'),
                    BASE_DIR / 'muya_wce' / 'static',
                    BASE_DIR / 'collation' / 'core' / 'static'
                    ]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
       },
   },
   'handlers': {
       'console': {
           'level': env('LOG_LEVEL_DJANGO'),
           'class': 'logging.StreamHandler',
           'stream': sys.stdout,
           'formatter': 'verbose'
       },
   },
   'loggers': {
       '': {
           'handlers': ['console'],
           'level': env('LOG_LEVEL_DJANGO'),
           'propagate': True,
       },
   },
}