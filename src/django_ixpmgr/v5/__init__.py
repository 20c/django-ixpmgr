from django.apps import AppConfig

class IxpManagerAppConfig(AppConfig):
    name = "django_ixpmgr.v5"
    # Must be unique, will conflict if two versions are used
    label = "django_ixpmgr"
