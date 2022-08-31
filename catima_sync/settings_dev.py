from .settings_base import *
from pathlib import Path

SECRET_KEY = "django-insecure-uhmd7d6$mr3ey0a"  # FIXME change this
DEBUG = True  # FIXME change this for production
ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

PUBLIC_ROOT = BASE_DIR / "public"
STATIC_ROOT = PUBLIC_ROOT / "static"
STATIC_URL = "static/"
