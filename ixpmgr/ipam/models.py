from django.db import models

import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *

# Create your models here.
class IpAddress(ixpmgr_models.Ipv4Address):
    class Meta: proxy=True
    proxies = ProxyManager()
    Source = ixpmgr_models.Ipv4Address
    objects_v6 = redirected_manager(ixpmgr_models.Ipv6Address)

    managing_account = NullField()
    consuming_account = NullField()
    external_ref = NullField()
    version = ConstField(4)
    # address = ProxyField(Source.address)
    pk = ProxyField(Source.address)
    prefix_length = ConstField(0)
    fqdn = NullField()
    valid_not_before = NullField()
    valid_not_after = NullField()


class MacAddress(models.Model):
    pass
