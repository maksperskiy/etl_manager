"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import time
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zd*-6h4u1rxok)9vywy!kr(d19#gm9u3ygn$m4h$ov30t2+kq1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # Your apps
    "common",
    "datasources",
    # Third-party apps
    "django_json_widget",
    "django_celery_beat",
    "storages",
    "django_extensions",
    "corsheaders",
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

CORS_ALLOW_ALL_ORIGINS = (
    True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]  # If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`
ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["./templates"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "datapipes"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "postgres"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru-RU"


TIME_ZONE = os.getenv("TZ", "UTC")

USE_I18N = True

USE_TZ = True


# Storage


config = dict(
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    endpoint_url=os.getenv("MINIO_URL"),
    region_name=os.getenv("MINIO_SITE_REGION"),
    signature_version="s3v4",
    bucket_name="datapipes",
    file_overwrite=False,
    default_acl=None,
    querystring_auth=False,
    use_ssl=False,
    object_parameters={
        "CacheControl": "max-age=86400",
    },
    url_protocol=os.getenv("MINIO_PROTOCOL", "http:"),
    custom_domain=os.getenv("MINIO_CUSTOM_DOMAIN", f"localhost:9005/datapipes"),
)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {**config},
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {**config},
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
# Celery configurations
CELERY_BROKER_URL = f"amqp://{RABBIT_HOST}:{RABBIT_PORT}//"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Optional: Specify the timezone if needed
CELERY_TIMEZONE = os.getenv("TZ", "UTC")

# Enable celery beat scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s",
            "datefmt": "%y %b %d, %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "celery": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "celery.log",
            "formatter": "simple",
            "maxBytes": 1024 * 1024 * 100,  # 100 mb
        },
    },
    "loggers": {
        "celery": {
            "handlers": ["celery", "console"],
            "level": "INFO",
        },
    },
}

from logging.config import dictConfig

dictConfig(LOGGING)

SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL")
