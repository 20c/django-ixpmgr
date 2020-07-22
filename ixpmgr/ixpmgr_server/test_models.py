from django.test import TestCase

from django_ixpmgr import models as ixpmgr_models
from ixpmgr_server.models import Account, BillingInformation, RegAddress


def make_chix():
    account = Account.proxies.create(
        name="ChIX",
        address=RegAddress.proxies.create(
            country="US",
            locality="Chicago",
            region="IL",
            postal_code="60605",
            # street_address="427 S. LaSalle", #todo
            address1="427 S. LaSalle",
        ),
        billing_information=BillingInformation.proxies.create(
            country="US",
            name="William",
            billingaddress1="123 Billings St.",
            locality="New York",
            region="NY",
            postal_code="28305",
        ),
    )
    location = ixpmgr_models.Location.objects.create(
        name="ChIX main",
        shortname="chix1",
        tag="chix",
        address="420 Michigan Ave",
        city="Chicago",
        country="US",
    )
    cabinet = ixpmgr_models.Cabinet.objects.create(
        locationid=location,
        name="chix main cabinet",
        cololocation="chix main coloc",
        height=42,
    )
    ixpmgr_models.Custkit.objects.create(
        custid=account, cabinetid=cabinet, name="chix kit",
    )
    return account


class AccountTestCase(TestCase):
    def setUp(self):
        self.acc1 = make_chix()

    def test_get(self):
        acc = Account.objects.get(pk=self.acc1.id)
        cust = ixpmgr_models.Cust.objects.get(pk=self.acc1.id)
        self.assertEqual(acc.name, "ChIX")
        self.assertEqual(cust.name, "ChIX")
