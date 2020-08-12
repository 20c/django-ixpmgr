import pytest
from django.conf import settings
import hypothesis
from hypothesis import strategies
import schemathesis
from schemathesis.models import Case

# Test the API conformance to the IX-API spec.
# schemathesis generates request data as "hypothesis" examples, and validates
# responses against a server (either running separately, or directly using wsgi app)

# Combines decorators to use specific example data
def example_for(path):
    def _dec(func):
        strat = schema[path]["GET"].as_strategy()
        endpoint = strat.example()
        endpoint.path_parameters = {"id": "1"}
        if USE_WSGI:
            strat = pytest.mark.django_db(strat)
        return hypothesis.given(strat)(
            hypothesis.example(endpoint)(func)
        )
    return _dec

# Always check for an id=1 object
@schemathesis.hooks.register
def before_add_examples(context, examples):
    examples.append(
        Case(endpoint=context.endpoint, path_parameters={'id': 1})
    )

hypothesis.settings.register_profile("main", deadline=None) # disable timeouts
hypothesis.settings.load_profile("main")


SOCKET_ADDR = "localhost:5000"
SCHEMA_PATH = "/static/schema/v2.json"
USE_WSGI = False

if USE_WSGI:
    # Use wsgi app - faster but has encoding issue? (fixme)
    from ixapi.wsgi import application
    schema = schemathesis.from_wsgi(SCHEMA_PATH, application)
else:
    # Use a running app - todo: how to use test data
    schema = schemathesis.from_uri(f"http://{SOCKET_ADDR}{SCHEMA_PATH}")

def _create_test(endpoint):
    @schema.parametrize(method="GET", endpoint=f"/{endpoint}")
    # @example_for(f"/{endpoint}" + "/{id}")
    def test_endpoint(case):
        response = case.call()
        case.validate_response(response)
        assert response.status_code < 500
    return test_endpoint

test_accounts = _create_test('accounts')
test_facilities = _create_test('facilities')

test_member_joining_rules = _create_test("member-joining-rules")
test_network_services = _create_test("network-services")
test_network_features = _create_test("network-features")
test_ips = _create_test("ips")
test_macs = _create_test("macs")
