import os, logging
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
ALLOWED_HOSTS = ["gamari-devs.com", "localhost"]

print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

GOOGLE_BOOKS_API_KEY = config("GOOGLE_BOOKS_API_KEY", default="")

APP_NAME = "Yommy"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Local
    "authentication.apps.AuthenticationConfig",
    "apps.book.apps.BookConfig",
    "apps.record.apps.RecordConfig",
    "apps.review.apps.ReviewConfig",
    "apps.follow.apps.FollowConfig",
    "apps.contact.apps.ContactConfig",
    "apps.ranking.apps.RankingConfig",
    "apps.selection.apps.SelectionConfig",
    "apps.search.apps.SearchConfig",
    "apps.management.apps.ManagementConfig",
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
    "allauth.account.middleware.AccountMiddleware",
]

# API側の設定
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "config/templates")],
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


# 認証関係

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID", default=""),
            "secret": config("GOOGLE_CLIENT_SECRET", default=""),
        },
        "SCOPE": [
            "profile",
            "email",
        ],
    }
}

LOGIN_REDIRECT_URL = "/mypage/"

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

AUTH_USER_MODEL = "authentication.Account"
LOGIN_URL = "login"
SOCIALACCOUNT_LOGIN_ON_GET = True

# ログ設定
LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "[{levelname}][{module}.{funcName}()] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/error.log'),
            "formatter": "verbose",
        },
        "time_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/time.log'),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "time_logger": {
            "handlers": ["time_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}

# 国際化設定

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_TZ = False
USE_I18N = True
USE_L10N = True


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# 環境差分の設定
if DEBUG:
    print("ローカル")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("本番環境")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    # POSTGRES_DB = config("POSTGRES_DB", default="")
    # POSTGRES_USER = config("POSTGRES_USER", default="")
    # POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="")
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': POSTGRES_DB,
    #         'USER': POSTGRES_USER,
    #         'PASSWORD': POSTGRES_PASSWORD,
    #         'HOST': 'db',
    #         'PORT': '5432',
    #     }
    # }
    # APP_URL = config("APP_URL", default="")
    # MEDIA_URL = f"{APP_URL}/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
