"""
Django settings for type_based_creator project.
"""
from pathlib import Path

import environ

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x@2eq$ii&yrkfdpwsk81okt!0fq0joe21i2svhjyy)v$3^*og@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: list[str] = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "type_based_creator.apps.AppConfig",
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "type_based_creator.handler.error_handler",
}

ROOT_URLCONF = "type_based_creator.urls"

WSGI_APPLICATION = "type_based_creator.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
