from django.db import models

from ixapi_schema.v2.constants import ipam as schema_const

import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *


class _IpMixin:
    # TODO: which interface?
    @property
    def _vlan_interface(self):
        """
        Return the Vlan interface
        """
        return ixpmgr_models.Vlaninterface.objects.filter(vlanid=self.vlanid).first()

    @_vlan_interface.setter
    def _vlan_interface(self, vlani: ixpmgr_models.Vlaninterface):
        """
        Set the Vlan interface
        """
        self.vlanid = vlani.vlanid


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

    @_customer.setter
    def _customer(self, custid):
        """
        Return the customer/account relationship for the network
        service through the Vlan interface
        """
        virti = ixpmgr_models.Virtualinterface.objects.filter(custid=custid).first()
        if not virti:
            raise ValueError("No virtual interface for customer", custid)
        vlani = ixpmgr_models.Vlaninterface.objects.filter(virtualinterfaceid=virti.id).first()
        if not vlani:
            raise ValueError("No VLAN interface for virtual interface", virti.id)
        self._vlan_interface = vlani


    # @proxies.property
    # def managing_account(self):
    #     return self._customer.id

    # @property
    # def consuming_account(self):
    #     # TODO: looks like managing and consuming are the same
    #     # in ixp manager? come back to this
    #     return self._customer.id

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
    # todo: special input handling, inserting different models
    version = proxies.const_field(schema_const.IpVersion.IPV4)

    @property
    def fqdn(self):
        vlani = self._vlan_interface
        if vlani: return self._vlan_interface.ipv4hostname

    valid_not_before = proxies.null_field()
    valid_not_after = proxies.null_field()
    pk = proxies.field(Source.address)
    #TODO: why isnt this happening through pk
    # id = proxies.field(Source.address)

    @proxies.property(Source.vlanid)
    def managing_account(self):
        return self._customer.id

    @managing_account.setter
    def managing_account(self, custid):
        self._customer = custid

    consuming_account = managing_account

class IpAddress6(ixpmgr_models.Ipv6Address, _IpMixin):
    class Meta: proxy=True
    proxies = ProxyManager()
    Source = ixpmgr_models.Ipv6Address
    version = proxies.const_field(schema_const.IpVersion.IPV6)


    @property
    def fqdn(self):
        vlani = self._vlan_interface
        if vlani: return self._vlan_interface.ipv6hostname

    valid_not_before = proxies.null_field()
    valid_not_after = proxies.null_field()
    pk = proxies.field(Source.address)
    #TODO: why isnt this happening through pk
    # id = proxies.field(Source.address)

    @proxies.property(Source.vlanid)
    def managing_account(self):
        return self._customer.id
    @managing_account.setter
    def managing_account(self, custid):
        self._customer = custid

    consuming_account = managing_account


# Simulated polymorphism: a dummy model with a multimanager for "subtypes"
class IpAddress(models.Model):
    objects = MultiManager(
        [IpAddress4.objects.all(), IpAddress6.objects.all()]
    )


class MacAddress(ixpmgr_models.Macaddress):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.Macaddress

    @proxies.property(Source.vlan_interface)
    def managing_account(self):
        virt = self.vlan_interface.virtualinterfaceid
        if virt: return virt.custid.id

    @managing_account.setter
    def managing_account(self, custid):
        # TODO: how to choose interfaces
        virti = ixpmgr_models.Virtualinterface.objects.filter(custid=custid).first()
        if not virti:
            raise ValueError("No virtual interface for customer", custid)
        vlani = ixpmgr_models.Vlaninterface.objects.filter(virtualinterfaceid=virti.id).first()
        if not vlani:
            raise ValueError("No VLAN interface for virtual interface", virti.id)
        self.vlan_interface = vlani

    consuming_account = managing_account

    external_ref = proxies.null_field()
    valid_not_before = proxies.null_field()
    valid_not_after = proxies.null_field()

    network_service_config = proxies.null_field()
    assigned_at = proxies.field(Source.created)

    @proxies.property(Source.mac)
    def address(self):
        """
        ixapi spec wants colon delimited mac addresses
        ixp manager stores without
        solution taken from: https://stackoverflow.com/a/11006780
        """
        return ':'.join(self.mac[i:i+2] for i in range(0,12,2))

    @address.setter
    def address(self, value: str):
        # breakpoint()
        if value.find(':') != -1:
            value = ''.join(value.split(':'))
        self.mac = value
