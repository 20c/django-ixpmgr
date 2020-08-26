"""
generated by `python manage.py diffsettings`

when regenerating grab the following properties and replace
them in the newly generated settings:

`DATABASES`
`MIGRATION_MODULES`
"""

import os

ALLOWED_HOSTS = ["*"]
APPEND_SLASH = False
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
BASE_DIR = os.path.dirname(__file__)  ###
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",},
    "ixpmanager": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",},
}
DATABASE_ROUTERS = ["django_ixpmgr.routers.Router"]
DEBUG = True
ERROR_DOCS_BASE_URL = "https://errors.ix-api.net/v2/"  ###
INSTALLED_APPS = [
    "crm",
    "catalog",
    "service",
    "ipam",
    "config",
    "django_ixpmgr.v57.IxpManagerConfig",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
IXAPI_NAMESPACES = ["crm", "catalog", "service", "ipam", "config"]  ###

MIGRATION_MODULES = dict([(name, None) for name in IXAPI_NAMESPACES])

IXPMANAGER_OPERATOR_NAME = None  ###
IXPMGR_APP = "django_ixpmgr.v57.IxpManagerConfig"  ###
IXPMGR_VERSION = "5.7"  ###
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": None,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}  ###
ROOT_URLCONF = "ixapi.urls"  ###
SECRET_KEY = "!tests"
SETTINGS_MODULE = "ixapi.settings"  ###
STATIC_ROOT = "/var/www/ixpmgr"
STATIC_URL = "static/"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
TIME_ZONE = "UTC"
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = "ixapi.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"stderr": {"level": "DEBUG", "class": "logging.StreamHandler",},},
    "loggers": {"": {"handlers": ["stderr"], "level": "DEBUG", "propagate": False},},
}
