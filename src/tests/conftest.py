from tests.django_init import django_configure

from tests.fixtures import *

def pytest_configure():
    django_configure()
