"""
Example Django settings for muya_wce project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
from pathlib import Path

if 'test' in sys.argv:
    TESTING = True
else:
    TESTING = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sw4h0owsl-78^9rhyfu4y84*e7j0hn5))7gp1xug-%47wp*um5'

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
    'django_celery_results',
    'accounts.apps.AccountsConfig',
    'transcriptions.apps.TranscriptionsConfig',
    'collation.apps.CollationConfig',
    'rest_framework',
    'api.apps.ApiConfig',
]

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

WSGI_APPLICATION = 'muya_wce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'user',
        'PASSWORD': 'pwrd',
        'HOST': '127.0.0.1'
    }
}

# user and login setup
LOGIN_URL = '/accounts/login/'
AUTH_USER_MODEL = 'accounts.User'
USER_IDENTIFIER_FIELD = 'full_name'

# django-rest-framework settings
REST_FRAMEWORK = {'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
                  'PAGE_SIZE': 100,
                  'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
                   ],
                  'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',)
                  }

# Celery setup
CELERY_BROKER_URL = 'amqp://me:example@localhost'
CELERY_RESULT_BACKEND = 'django-db'

# local file based email system
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# export directories
APPARATUS_BASE_DIR = BASE_DIR / 'apparatus'
EXPORT_BASE_DIR = BASE_DIR / 'exports'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
                    ('common', BASE_DIR / 'common-static'),
                    BASE_DIR / 'muya_wce' / 'static',
                    BASE_DIR / 'collation' / 'core' / 'static'
                    ]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
