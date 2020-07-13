from django.test import TestCase

from ixpmgr_server.models import Account, BillingInformation, RegAddress

def make_chix():
    a = Account.create(
        name="ChIX",
        address=RegAddress.create(
            country="US",
            locality="Chicago",
            region="IL",
            postal_code="60605",
            # street_address="427 S. LaSalle",
            address1="427 S. LaSalle",
        ),
        billing_information=BillingInformation.create(
            country="US",
            billingaddress1="123 Billings St.",
            locality="New York",
            # region="NY",
            postal_code="28305",
        )
    )
    return a

class AccountTestCase(TestCase):
    def setUp(self):
        a = make_chix()
        a.save()
