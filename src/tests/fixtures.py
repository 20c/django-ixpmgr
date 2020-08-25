import os
import pytest
import json


@pytest.fixture
def ixpmgr_models():
    """
    return models module for django-ixpmgr-ixapi

    TODO: currently hardcoded to v56, should support
    parametrizing by version
    """
    import django_ixpmgr.v57.models as v57_models
    return v57_models


@pytest.fixture
def ixpmgr_data():
    """
    import initial ixp manager data

    TODO: currently hard-coded to v56, should support
    parametrizing versions or something
    """
    from django.core.management import call_command

    path = os.path.join(os.path.dirname(__file__), "data", "v56", "init.json")
    print(f"Loading from {path}")

    # create tables
    call_command("migrate", "ixpmgr", run_syncdb=True, database="ixpmanager")

    # load initial data
    call_command("loaddata", path, app="ixpmgr", database="ixpmanager")

    with open(path) as json_data:
        data = json.load(json_data)
    return format_data(data)

def format_data(data):
    formatted_data = {}
    for instance in data:
        model = instance["model"]
        pk = instance["pk"]
        fields = instance["fields"]
        if model not in formatted_data:
            formatted_data[model] = {}
        formatted_data[model][pk] = fields
    return formatted_data



 