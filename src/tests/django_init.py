from django.conf import settings
from tests import django_settings

def django_configure():
    settings.configure(**vars(django_settings))
