import pytest

import ixapi.models

@pytest.mark.django_db
def test_something(ixpmgr_data, ixpmgr_models):
    assert ixapi.models.MacAddress.objects.count() == 2
    assert ixpmgr_models.L2Address.objects.count() == 2
