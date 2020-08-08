from django.test import TestCase

from django_ixpmgr.v57 import (
    models as ixpmgr_models,
    const as ixpmgr_const,
)
from ixapi.models import (
    Account, BillingInformation, RegAddress,
    Facility,
    ExchangeLanNetworkService, AllowMemberJoiningRule,
    RouteServerNetworkFeature,
)

# give account a location
def make_custkit(locname):
    location = ixpmgr_models.Location.objects.get_or_create(
        shortname=locname,
        name="ChIX main",
        tag="chix",
        address="420 Michigan Ave",
        city="Chicago",
        country="US",
    )
    cabinet = ixpmgr_models.Cabinet.objects.get_or_create(
        locationid=location,
        name="chix main cabinet",
        cololocation="chix main coloc",
        height=42,
    )
    ixpmgr_models.Custkit.objects.create(
        custid=account, cabinetid=cabinet, name="chix kit",
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
    location_shortname = "chix1"
    return account

def make_ixp():
    return ixpmgr_models.Ixp.objects.create()

# or make_infrastructure
def make_exchangelan(acc: Account, ixp=None):
    if not ixp:
        ixp = make_ixp()
    # set account
    c2ixp = ixpmgr_models.CustomerToIxp.objects.create(customer=acc, ixp=ixp)

    return ExchangeLanNetworkService.proxies.create(
        name = acc.name + " exchange_lan",
        peeringdb_ixid=42,
        ixp=ixp,
    )

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
    rs, _ = RouteServerNetworkFeature.objects.get_or_create(
        handle=handle,
        vlan=vlan,
        protocol=protocol,
        asn=asn,
    )
    return rs


def make_all():
    addr = "1.2.3.4"
    routerhandle = "handle1"
    acc = make_chix_account()
    el = make_exchangelan(acc)
    ip = make_ip(addr)
    vlan = make_vlan(el, ip)
    rout = make_routeserver(routerhandle, vlan)

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
        acc = make_chix_account()
        self.ixp = make_ixp()
        self.xlan = make_exchangelan(acc, self.ixp)

    def test_get(self):
        xlan = ExchangeLanNetworkService.objects.get(pk=self.xlan.id)
        infra = ixpmgr_models.Infrastructure.objects.get(pk=self.xlan.id)
        self.assertEqual(xlan.peeringdb_ixid, 42)
        self.assertEqual(xlan.ixp, self.ixp)


class RouteServerNetworkFeatureTestCase(ExchangeLanNetworkServiceTestCase):
    databases = ('ixpmanager', 'default')

    def setUp(self):
        super().setUp()
        Router = ixpmgr_const.Router
        protocol = Router.PROTOCOL_IPV4
        ip = make_ip("1.2.3.4")
        self.vlan = make_vlan(self.xlan, ip)
        self.rs = make_routeserver("rs1", self.vlan, protocol)

    def test_get(self):
        features = self.xlan.network_features
        self.assertEqual(self.vlan, self.rs.vlan)
        self.assertTrue(self.rs in features)
