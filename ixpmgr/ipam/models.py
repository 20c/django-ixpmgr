from django.db import models

from ixapi_schema.v2.constants import ipam as schema_const

import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *


# Proxy pk to address, so it's visible in shallow output lists
# todo: DRY up with mixin

class IpAddress4(ixpmgr_models.Ipv4Address):
    class Meta: proxy=True
    Source = ixpmgr_models.Ipv4Address
    proxies = ProxyManager()

    version = ConstField(schema_const.IpVersion.IPV4)
    prefix_length = ConstField(0)
    fqdn = NullField()
    valid_not_before = NullField()
    valid_not_after = NullField()
    managing_account = NullField()
    consuming_account = NullField()
    pk = ProxyField(Source.address)

class IpAddress6(ixpmgr_models.Ipv6Address):
    class Meta: proxy=True
    proxies = ProxyManager()
    Source = ixpmgr_models.Ipv6Address

    version = ConstField(schema_const.IpVersion.IPV6)
    prefix_length = ConstField(0)
    fqdn = NullField()
    valid_not_before = NullField()
    valid_not_after = NullField()
    managing_account = NullField()
    consuming_account = NullField()
    pk = ProxyField(Source.address)

class IpAddress(models.Model):
    objects = MultiManager(
        [IpAddress4.objects.all(), IpAddress6.objects.all()]
    )


class MacAddress(models.Model):
    pass
