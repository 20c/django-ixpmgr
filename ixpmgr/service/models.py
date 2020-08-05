from itertools import chain
from typing import List

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ixapi_schema.v2 import (
    entities as schema_entities,
    constants as schema_constants,
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
    # XXX: where is this used?
    # why not abstract?

class NetworkServiceBase:

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



class ExchangeLanNetworkService(NetworkServiceBase, ixpmgr_models.Infrastructure):
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
            RouteserverNetworkFeature.objects.filter(vlan=vlan).all()
            for vlan in self.vlan_set.all()
        )
        return list(chain(*qsets))


    @property
    def managing_account(self):
        return self._customer.id

    @property
    def consuming_account(self):
        # TODO: looks like managing and consuming are the same
        # in ixp manager? come back to this
        return self._customer.id

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
        ip_addresses = []
        for vlan in self.vlan_set.filter(private=0):
            addrs_v4 = ipam_models.IpAddress.objects.filter(vlanid=vlan.id)
            addrs_v6 = ipam_models.IpAddress.objects_v6.filter(vlanid=vlan.id)
            ip_addresses.extend(addrs_v4)
            ip_addresses.extend(addrs_v6)
        return ip_addresses

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


class RouteserverNetworkFeature(ixpmgr_models.Routers):
    proxies = ProxyManager()
    class Meta: proxy = True
    Source = ixpmgr_models.Infrastructure

    # asn inherited
    fqdn = ConstField("example.com")
    required = ConstField(False)
    nfc_required_contact_roles = NullField()

    @property
    def network_service(self):
        try:
            return ExchangeLanNetworkService.objects.get(vlan=self.vlan)
        except ObjectDoesNotExist:
            return None

    looking_glass_url = ConstField("https://lg.moon-ix.net/rs1")

    @property
    def address_families(self) -> List[str]:
        AddressFamilies = schema_constants.ipam.AddressFamilies
        afs = {
            ixpmgr_const.Router.PROTOCOL_IPV4: AddressFamilies.AF_INET,
            ixpmgr_const.Router.PROTOCOL_IPV6: AddressFamilies.AF_INET6,
        }
        return [afs[self.protocol]]

    session_mode = ConstField("public")
    available_bgp_session_types = NullField()
    ips = NullField()

    def save(self, *a, **k):
        self.type = ixpmgr_const.Router.TYPE_ROUTE_SERVER
        self.api_type = ixpmgr_const.Router.API_TYPE_NONE
        self.quarantine = 0
        self.bgp_lc = 0
        self.bgp_lc = 0
        self.rpki = 0
        self.rfc1997_passthru = 0
        self.skip_md5 = 0
        super().save()


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
