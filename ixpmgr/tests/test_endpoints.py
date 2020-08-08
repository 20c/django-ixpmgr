from pathlib import Path
import pytest

from django.conf import settings
import hypothesis
# from hypothesis import given, example
import schemathesis

from ixapi.wsgi import application


hypothesis.settings.register_profile("poop", deadline=None)
hypothesis.settings.load_profile("poop")

schema = schemathesis.from_uri("http://localhost:5000/static/schema/v2.json")

# schema_path = Path(settings.BASE_DIR) / "static/schema/v2.json"
# schema = schemathesis.from_file(schema_path.open())

# schema = schemathesis.from_wsgi("/static/schema/v2.json", application)

def example_for(path):
    def _dec(func):
        strat = schema[path]["GET"].as_strategy()
        endpoint = strat.example()
        endpoint.path_parameters = {"id": "1"}
        return hypothesis.given(strat)(
            hypothesis.example(endpoint)(func)
        )
    return _dec

# get_account_strat = schema["/accounts/{id}"]["GET"].as_strategy()
# get_account = get_account_strat.example()
# get_account.path_parameters = {"id": "1"}

# @pytest.mark.django_db # need for wsgi
# @given(get_account_strat)
# @example(get_account)
# @schema.parametrize(method="GET", endpoint="/accounts")
@example_for("/accounts/{id}")
def test_accounts(case):
    response = case.call()
    case.validate_response(response)
    assert response.status_code < 500
