from django.test import TestCase

from django_ixpmgr.v57 import (
    models as ixpmgr_models,
    const as ixpmgr_const,
)
from ixapi.models import (
    Account, BillingInformation, RegAddress,
    Facility,
    ExchangeLanNetworkService, AllowMemberJoiningRule,
    RouteserverNetworkFeature,
)


def make_chix_account():
    account = Account.proxies.create(
        name="ChIX",
        status=1, # todo - "normal" status?
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
            # region="NY",
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
    return ixpmgr_models.Ipv4Address.objects.create(address=addr)

def make_vlan(xlan, ip):
    vlan = ixpmgr_models.Vlan.objects.create(
        infrastructureid=xlan,
        private=False,
        peering_matrix=0,
        peering_manager=0)
    vlan.ipv4address_set.add(ip)
    return vlan

def make_routeserver(handle, vlan, protocol=4, asn="69"):
    rs = RouteserverNetworkFeature.objects.create(
        handle=handle,
        vlan=vlan, protocol=protocol, asn=asn,
    )
    return rs


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


class RouteserverNetworkFeatureTestCase(ExchangeLanNetworkServiceTestCase):
    databases = ('ixpmanager', 'default')

    def setUp(self):
        super().setUp()
        Router = ixpmgr_const.Router
        protocol = Router.PROTOCOL_IPV4
        ip = make_ip("1.2.3.4")
        self.vlan = make_vlan(self.xlan, ip)
        self.rs = make_routeserver(
            "handle1",
            self.vlan, protocol)

    def test_get(self):
        features = self.xlan.network_features
        self.assertEqual(self.vlan, self.rs.vlan)
        self.assertTrue(self.rs in features)
