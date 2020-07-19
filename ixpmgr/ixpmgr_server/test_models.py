from django.test import TestCase

from ixpmgr_server.models import Account, BillingInformation, RegAddress
from django_ixpmgr import models as ixpmodels

def make_chix():
    acc = Account.proxies.create(
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
        )
    )
    loc = ixpmodels.Location.objects.create(
        name="ChIX main",
        shortname="chix1",
        tag="chix",
        address = "420 Michigan Ave",
        city = "Chicago",
        country = "US",
    )
    cab = ixpmodels.Cabinet.objects.create(
        locationid = loc,
        name = "chix main cab",
        cololocation = "chix main coloc",
        height = 42,
    )
    k = ixpmodels.Custkit.objects.create(
        custid=acc,
        cabinetid=cab,
        name = "chix kit",
    )
    return acc

class AccountTestCase(TestCase):
    def setUp(self):
        a = make_chix()
        a.save()
