from django.test import TestCase

from django_ixpmgr import models as ixpmgr_models
from ixpmgr_server.models import Account, BillingInformation, RegAddress
from ixpmgr_server.models import Facility
from ixpmgr_server.models import ExchangeLanNetworkService, AllowMemberJoiningRule


def make_chix_account():
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

def make_ixp():
    return ixpmgr_models.Ixp.objects.create()

def make_exchangelan(ixp=None):
    if not ixp: ixp = make_ixp()
    xlan = ExchangeLanNetworkService.proxies.create(
        peeringdb_ixid=42,
        ixp=ixp,
    )
    return xlan

def make_ip(addr):
    return ixpmgr_models.Ipv4Address.objects.create(address="1.2.3.4")

def make_vlan(xlan, ip):
    vlan = ixpmgr_models.Vlan.objects.create(
        infrastructureid=xlan,
        private=False,
        peering_matrix=0,
        peering_manager=0)
    vlan.ipv4address_set.add(ip)
    return vlan

class AccountTestCase(TestCase):
    databases = ('ixpmanager', 'default')

    def setUp(self):
        self.acc1 = make_chix_account()

    def test_get(self):
        acc = Account.objects.get(pk=self.acc1.id)
        cust = ixpmgr_models.Cust.objects.get(pk=self.acc1.id)
        self.assertEqual(acc.name, "ChIX")
        self.assertEqual(cust.name, "ChIX")

class ExchangeLanNetworkServiceTestCase(TestCase):
    databases = ('ixpmanager', 'default')

    def setUp(self):
        self.ixp = make_ixp()
        self.xlan = make_exchangelan(self.ixp)

    def test_get(self):
        xlan = ExchangeLanNetworkService.objects.get(pk=self.xlan.id)
        infra = ixpmgr_models.Infrastructure.objects.get(pk=self.xlan.id)
        self.assertEqual(xlan.peeringdb_ixid, 42)
        self.assertEqual(xlan.ixp, self.ixp)
