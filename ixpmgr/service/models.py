from django.db import models

import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *

from crm import models as crm_models

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

class DenyMemberJoiningRule(models.Model):
    # class Meta: proxy = True
    Source = ixpmgr_models.Cust
    # type = ConstField('blacklist')


class NetworkService(models.Model): pass

class ExchangeLanNetworkService(ixpmgr_models.Infrastructure,):
    proxies = ProxyManager()
    class Meta: proxy = True
    Source = ixpmgr_models.Infrastructure
    # proxy_source = models.OneToOneField(Source, on_delete=models.CASCADE, primary_key=True)

    managing_account = NullField()
    consuming_account = NullField()
    external_ref = NullField()

    # name => shortname?
    metro_area = ConstField("IDK")
    network_features = NullField()
    product_offering = NullField()
    all_nsc_required_contact_roles = NullField()
    ip_addresses = NullField()
    peeringdb_ixid = ProxyField(Source.peeringdb_ix_id)
    ixfdb_ixid = ProxyField(Source.ixf_ix_id)
    # state = NullField()
    # status = NullField()

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
