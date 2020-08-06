from itertools import chain
from typing import List

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ixapi_schema.v2 import entities as schema_entities
from ixapi_schema.v2.constants import (
    config as config_const, ipam as ipam_const
)

from django_ixpmgr.v57 import (
    models as ixpmgr_models,
    const as ixpmgr_const,
)
from django_ixpmgr.model_util import *

from crm import models as crm_models
from ipam import models as ipam_models

# "Polymorphic" models: concrete inheritance to build multiple proxy models,
# which are collated by serializers

class MemberJoiningRule(models.Model): pass

class AllowMemberJoiningRule(ixpmgr_models.Cust):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.Cust

    managing_account = NullField()
    consuming_account = NullField()
    network_service = NullField()

    test_cust_name = ProxyField(Source.name)
    capacity_min = NullField()
    capacity_max = NullField()
    # type = ConstField('whitelist')

class DenyMemberJoiningRule(models.Model): pass
    # class Meta: proxy = True
    # Source = ixpmgr_models.Cust
    # type = ConstField('blacklist')


class NetworkService(models.Model): pass

class _NetworkServiceCustomer:
    @property
    def _customer(self):
        """
        Return the customer/account relationship for the network
        service through customertoixp
        """
        custixp = ixpmgr_models.CustomerToIxp.objects.filter(ixp=self.ixp).first()
        if not custixp:
            return None
        return custixp.customer


class ExchangeLanNetworkService(ixpmgr_models.Infrastructure, _NetworkServiceCustomer):
    proxies = ProxyManager()
    class Meta: proxy = True
    Source = ixpmgr_models.Infrastructure

    external_ref = NullField()

    # name => shortname?
    metro_area = ConstField("IDK")
    product_offering = NullField()
    all_nsc_required_contact_roles = NullField()
    peeringdb_ixid = ProxyField(Source.peeringdb_ix_id)
    ixfdb_ixid = ProxyField(Source.ixf_ix_id)
    status = NullField()

    @property
    def network_features(self):
        qsets = (
            RouteServerNetworkFeature.objects.filter(vlan=vlan).all()
            for vlan in self.vlan_set.all()
        )
        return list(chain(*qsets))


    @property
    def managing_account(self):
        return self._customer

    @property
    def consuming_account(self):
        # TODO: looks like managing and consuming are the same
        # in ixp manager? come back to this
        return self._customer

    @property
    def type(self):
        return "exchange_lan"

    @property
    def state(self):
        State = schema_entities.events.State
        source_state_map = {
            # todo - placeholder values for cust status
            0: State.DECOMMISSIONED,
            1: State.PRODUCTION,     # normal
            2: State.ARCHIVED,       # suspended
        }
        customer = self._customer

        if not customer:
            return None

        cust_status = customer.status

        if cust_status is None:
            return None

        return source_state_map[cust_status]

    @property
    def ip_addresses(self):
        # todo - check vlaninterface.ipvXenabled?
        # todo - exclude vlan.private>0 ?
        ipv4 = []
        for vlan in self.vlan_set.all():
            addrs = ipam_models.IpAddress.objects.filter(vlanid=vlan.id)
            ipv4.extend(addrs)
        return ipv4

    def save(self, *args, **kwargs):
        self.isprimary = True
        super().save(*args, **kwargs)

class P2PNetworkService(models.Model): pass
class P2MPNetworkService(models.Model): pass
class MP2MPNetworkService(models.Model): pass
class CloudNetworkService(models.Model): pass


# Features
class NetworkFeature(models.Model):
    pass


class RouteServerNetworkFeature(ixpmgr_models.Routers):
    proxies = ProxyManager()
    class Meta: proxy = True
    Source = ixpmgr_models.Infrastructure

    # asn inherited
    fqdn = ConstField("example.com") # todo - which vlan iface?
    required = ConstField(False)
    all_nfc_required_contact_roles = NullField()

    @property
    def ixp_specific_flags(self):
        flags = []
        if self.rpki:
            flags.append({"name": str(self.rpki), "description": "RPKI is available"})
        return flags

    @property
    def network_service(self):
        try:
            return ExchangeLanNetworkService.objects.get(vlan=self.vlan)
        except ObjectDoesNotExist:
            return None

    looking_glass_url = ConstField("https://lg.moon-ix.net/rs1")

    @property
    def address_families(self) -> List[str]:
        AddressFamilies = ipam_const.AddressFamilies
        afs = {
            ixpmgr_const.Router.PROTOCOL_IPV4: AddressFamilies.AF_INET,
            ixpmgr_const.Router.PROTOCOL_IPV6: AddressFamilies.AF_INET6,
        }
        return [afs[self.protocol]]

    session_mode = ConstField(config_const.RouteServerSessionMode.MODE_PUBLIC)
    available_bgp_session_types = NullField()

    @property
    def ip_addresses(self):
        # todo - check vlaninterface.ipvXenabled?
        ipv4 = []
        for vlan in self.vlan_set.all():
            addrs = ipam_models.IpAddress.objects.filter(vlanid=vlan.id)
            ipv4.extend(addrs)
        return ipv4

    def save(self, *a, **k):
        self.type = ixpmgr_const.Router.TYPE_ROUTE_SERVER
        self.api_type = ixpmgr_const.Router.API_TYPE_NONE
        self.quarantine = 0
        self.bgp_lc = 0
        self.rfc1997_passthru = 0
        self.skip_md5 = 0
        if self.rpki is None: self.rpki = 0
        super().save(*args, **kwargs)


class BlackholingNetworkFeature(models.Model):
    pass


class IXPRouterNetworkFeature(models.Model):
    pass


class WhitelistMemberJoiningRule(models.Model):
    pass


class BlacklistMemberJoiningRule(models.Model):
    pass



class ExchangeLanNetworkProductOffering(models.Model):
    pass



class MP2MPNetworkProductOffering(models.Model):
    pass
