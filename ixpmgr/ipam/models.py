from django.db import models

from ixapi_schema.v2.constants import ipam as schema_const

import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *


class _IpMixin:
    # fqdn = NullField()
    # valid_not_before = NullField()
    # valid_not_after = NullField()
    # managing_account = NullField()
    # consuming_account = NullField()

    @property
    def _vlan_interface(self):
        """
        Return the Vlan interface
        """
        return ixpmgr_models.Vlaninterface.objects.filter(vlanid=self.vlanid).first()

    @property
    def _network_info(self):
        """
        Return network information
        """

        try:
            netinfo = ixpmgr_models.Networkinfo.objects.get(
                vlanid=self.vlanid, network=self.address
            )
            return netinfo
        except ixpmgr_models.Networkinfo.DoesNotExist:
            return None

    @property
    def _customer(self):
        """
        Return the customer/account relationship for the network
        service through the Vlan interface
        """
        iface = self._vlan_interface
        if iface: return iface.virtualinterfaceid.custid

    @property
    def managing_account(self):
        return self._customer.id

    @property
    def consuming_account(self):
        # TODO: looks like managing and consuming are the same
        # in ixp manager? come back to this
        return self._customer.id

    @property
    def prefix_length(self):
        netinfo = self._network_info
        if netinfo:
            return netinfo.masklen
        return None


# Proxy pk to address, so it's visible in shallow output lists
# todo: DRY up with mixin

class IpAddress4(ixpmgr_models.Ipv4Address, _IpMixin):

    class Meta: proxy=True
    Source = ixpmgr_models.Ipv4Address
    proxies = ProxyManager()

    version = ConstField(schema_const.IpVersion.IPV4)

    @property
    def fqdn(self):
        vlani = self._vlan_interface
        if vlani: return self._vlan_interface.ipv4hostname

    valid_not_before = NullField()
    valid_not_after = NullField()
    pk = ProxyField(Source.address)
    #TODO: why isnt this happening through pk
    id = ProxyField(Source.address)

class IpAddress6(ixpmgr_models.Ipv6Address, _IpMixin):
    class Meta: proxy=True
    proxies = ProxyManager()
    Source = ixpmgr_models.Ipv6Address

    version = ConstField(schema_const.IpVersion.IPV6)

    @property
    def fqdn(self):
        vlani = self._vlan_interface
        if vlani: return self._vlan_interface.ipv6hostname

    valid_not_before = NullField()
    valid_not_after = NullField()
    pk = ProxyField(Source.address)
    #TODO: why isnt this happening through pk
    id = ProxyField(Source.address)


# Simulated polymorphism: a dummy model with a multimanager for "subtypes"
class IpAddress(models.Model):
    objects = MultiManager(
        [IpAddress4.objects.all(), IpAddress6.objects.all()]
    )


class MacAddress(models.Model):
    pass
