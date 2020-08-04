from django.db import models

from ixapi_schema.v2.entities.events import State

import django_ixpmgr.v57.models as ixpmgr_models
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

class ExchangeLanNetworkService(ixpmgr_models.Infrastructure,):
    proxies = ProxyManager()
    class Meta: proxy = True
    Source = ixpmgr_models.Infrastructure

    managing_account = NullField()
    consuming_account = NullField()
    external_ref = NullField()

    # name => shortname?
    metro_area = ConstField("IDK")
    network_features = NullField()
    product_offering = NullField()
    all_nsc_required_contact_roles = NullField()

    peeringdb_ixid = ProxyField(Source.peeringdb_ix_id)
    ixfdb_ixid = ProxyField(Source.ixf_ix_id)

    @property
    def state(self):
        # todo - placeholder values for cust status
        source_state_map = {
            0: State.DECOMMISSIONED, # not commissioned
            1: State.PRODUCTION, # normal
            2: State.ARCHIVED, # suspended
        }
        custixp = ixpmgr_models.CustomerToIxp.objects.filter(ixp=self.ixp).first()
        cust_status = custixp.customer.status
        if cust_status is None: return None
        return source_state_map[cust_status]

    status = NullField()

    @property
    def ip_addresses(self):
        ipv4 = []
        for vlan in self.vlan_set.all():
            addrs = ipam_models.IpAddress.objects.filter(vlanid=vlan.id)
            # addrs = vlan.ipv4address_set.all()
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


class BlackholingNetworkFeature(models.Model):
    pass


class RouteserverNetworkFeature(models.Model):
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
