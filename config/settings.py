"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

from django.urls import reverse_lazy
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1y&&k$ibx!x6^jlgdo2g(wtcy%!x^t3hjor@^%7!6cz8c5t@vv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', [])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', [])

CORS_ALLOW_ALL_ORIGINS = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "corsheaders",

    "app_habits",
    "app_telegrambot",
    "app_social_auth",
    "app_accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (

    ),
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'JWT': {
            'description': 'Bearer <token>',
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    }
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": env.str("DB_NAME", "coursework_7"),
        "USER": env.str("DB_USER", "postgres"),
        "PASSWORD": env.str("DB_PASSWORD", ""),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.int("DB_PORT", 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPLICATION_SCHEME = env.str('APPLICATION_SCHEME', 'https')
APPLICATION_HOSTNAME = env.str('APPLICATION_HOSTNAME', 'localhost')
if APPLICATION_HOSTNAME:
    ALLOWED_HOSTS.append(APPLICATION_HOSTNAME)
    CORS_ALLOWED_ORIGINS.append(f'{APPLICATION_SCHEME}://{APPLICATION_HOSTNAME}')
    CSRF_TRUSTED_ORIGINS.append(f'{APPLICATION_SCHEME}://{APPLICATION_HOSTNAME}')

TELEGRAM_USE_POLL = env.bool('TELEGRAM_USE_POLL', False)
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', None)

CELERY_TIMEZONE = TIME_ZONE

CELERY_TASK_TRACK_STARTED = env.bool('CELERY_TASK_TRACK_STARTED', True)
CELERY_TASK_TIME_LIMIT = env.int('CELERY_TASK_TIME_LIMIT', 60 * 30)

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

CELERY_BEAT_SCHEDULE = {}

TELEGRAM_POLL_INTERVAL = env.int('TELEGRAM_POLL_INTERVAL', 10)

MAX_OAUTH_TIMEOUT = env.int('MAX_OAUTH_TIMEOUT', 86400)

LOGOUT_REDIRECT_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = '/'
