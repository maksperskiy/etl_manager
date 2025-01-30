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
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
    "common",
    # Third-party apps
    "django_celery_beat",
    "storages",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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


# from django.templatetags.static import static
from django.urls import reverse_lazy

UNFOLD = {
    # "SITE_TITLE": "Custom suffix in <title> tag",
    # "SITE_HEADER": "Appears in sidebar at the top",
    # "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    # "SITE_SYMBOL": "speed",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("favicon.svg"),
    #     },
    # ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": False,  # show/hide "View on site" button, default: True
    # "ENVIRONMENT": "sample_app.environment_callback",
    # "DASHBOARD_CALLBACK": "datapipes.views.dashboard_callback",
    # "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
    # "LOGIN": {
    #     "image": lambda request: static("sample/login-bg.jpg"),
    #     "redirect_after": lambda request: reverse_lazy("admin:datapipes_changelist"),
    # },
    # "STYLES": [
    #     lambda request: static("css/style.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    "COLORS": {
        "font": {
            "subtle-light": "107 120 128",
            "subtle-dark": "156 170 175",
            "default-light": "75 89 99",
            "default-dark": "209 216 219",
            "important-light": "17 35 39",
            "important-dark": "243 245 246",
        },
        "primary": {
            "50": "221 239 254",
            "100": "194 228 253",
            "200": "168 216 252",
            "300": "137 193 250",
            "400": "109 170 234",
            "500": "81 146 221",
            "600": "49 113 196",
            "700": "17 81 170",
            "800": "13 53 113",
            "900": "8 36 75",
            "950": "0 0 0",
        },
    },
    # "EXTENSIONS": {
    # },
    # "SIDEBAR": {
    #     "show_search": False,  # Search in applications and models names
    #     "show_all_applications": False,  # Dropdown with all applications and models
    #     "navigation": [
    #         {
    #             "title": "Navigation",
    #             "separator": True,  # Top border
    #             "collapsible": False,  # Collapsible group of links
    #             "items": [
    #                 {
    #                     "title": "Dashboard",
    #                     "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
    #                     "link": reverse_lazy("admin:index"),
    #                     # "badge": "datapipes.badge_callback",
    #                     # "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": "Cameras",
    #                     "icon": "videocam",  # Supported icon set: https://fonts.google.com/icons
    #                     "link": reverse_lazy("admin:datapipes_camera_changelist"),
    #                     # "badge": "datapipes.badge_callback",
    #                     # "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": "Alerts",
    #                     "icon": "campaign",  # Supported icon set: https://fonts.google.com/icons
    #                     "link": reverse_lazy("admin:app_list", kwargs={"app_label": "alert"}),
    #                     # "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": "Users",
    #                     "icon": "people",
    #                     "link": reverse_lazy("admin:app_list", kwargs={"app_label": "auth"}),
    #                     # "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": "Storages",
    #                     "icon": "cloud_upload",
    #                     "link": reverse_lazy("admin:common_s3config_changelist"),
    #                     # "permission": lambda request: request.user.is_superuser,
    #                 },
    #             ],
    #         },
    #     ],
    # },
    # "TABS": [
    #     {
    #         "models": [
    #             "datapipes.camera",
    #             "datapipes.tag",
    #         ],
    #         "items": [
    #             {
    #                 "title": "Cameras",
    #                 "link": reverse_lazy("admin:datapipes_camera_changelist"),
    #                 # "permission": "datapipes.permission_callback",
    #             },
    #             {
    #                 "title": "Tags",
    #                 "link": reverse_lazy("admin:datapipes_tag_changelist"),
    #                 # "permission": lambda request: request.user.is_superuser,
    #             },
    #         ],
    #     },
    # ],
}
