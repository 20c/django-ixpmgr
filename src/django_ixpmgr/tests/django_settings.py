import os
from django.conf import settings

IXPMGR_VERSION = os.environ["IXPMGR_VERSION"]
SECRET_KEY = "test-secret-key"
INSTALLED_APPS = [
    "django_ixpmgr.IxpManagerAppConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]
