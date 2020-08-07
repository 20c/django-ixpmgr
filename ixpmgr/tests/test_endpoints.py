from pathlib import Path
import pytest

from django.conf import settings
import schemathesis

from ixapi.wsgi import application


# schema_path = Path(settings.BASE_DIR) / "static/schema/v2.json"
# schema = schemathesis.from_file(schema_path.open())
schema = schemathesis.from_wsgi("/static/schema/v2.json", application)

@pytest.mark.django_db
@schema.parametrize(method="GET", endpoint="/accounts")
def test_accounts(case):
    response = case.call_wsgi()
    case.validate_response(response)
    assert response.status_code < 500
