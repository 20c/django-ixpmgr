from django.db import models
from ixapi_schema.v2 import entities as schema_entities
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *

import service.models as service_models
import ipam.models as ipam_models

class Connection(ixpmgr_models.Virtualinterface):

    """
    A Connection is a functional group of physical connections collected together into a LAG (aka trunk).

    A connection with only one port can be also configured as standalone which means no LAG configuration on the switch.

    Currently only implemented in the most basic form so we can reference
    it in the ExchangeLanNetworkServiceConfig model
    """

    proxies = ProxyManager()
    Source = ixpmgr_models.Virtualinterface
    class Meta:
        proxy = True


    """
    state = NullField()
    status = NullField()
    managing_account = NullField()
    consuming_account = NullField()
    billing_account = NullField()
    purchase_order = NullField()
    external_ref = NullField()
    contract_ref = NullField()
    role_assignments = NullField()
    mode = NullField()
    lacp_timeout = NullField()
    speed = NullField()
    name = NullField()
    ports = NullField()
    vlan_types = NullField()
    outer_vlan_ethertypes = NullField()
    """

class ExchangeLanNetworkServiceConfig(ixpmgr_models.Vlaninterface):

    """
    A NetworkServiceConfig is a customer's configuration for usage of a NetworkService, e.g. the configuration of a (subset of a) connection for that customer's traffic
    """

    proxies = ProxyManager()
    Source = ixpmgr_models.Vlaninterface
    class Meta:
        proxy = True

    contract_ref = NullField()
    purchase_order = NullField()

    @property
    def _customer(self):
        """
        helper function to get the related IXPMGR customer object
        """
        return self.virtualinterfaceid.custid

    @property
    def _connection(self):
        """
        helper function to get the related IXAPI connection object
        """
        return Connection.objects.get(id=self.virtualinterfaceid.id)

    @property
    def _network_service(self):
        """
        helper function to get the related IXAPI networkservice object
        """
        return service_models.ExchangeLanNetworkService.objects.get(id=self.vlanid.infrastructureid.id)

    @property
    def _physical(self):
        """
        helper function to get the related IXPMGR physicalinterface object
        """
        return ixpmgr_models.Physicalinterface.objects.get(
            virtualinterfaceid=self.virtualinterfaceid
        )

    @property
    def _switch(self):
        """
        helper function to get the related IXPMGR switch object
        """
        return self._physical.switchportid.switchid


    @property
    def capacity(self):

        # the only specification of speed / capacity
        # we found in the ixp manager schema is
        # directly on the physical interface, so this what
        # we pass through for now - may need to take a close
        # look at this

        return self._physical.speed

    @property
    def state(self):
        State = schema_entities.events.State
        ns_state = self._network_service.state
        phy_state = self._physical.status

        # if network-service state is anything but
        # PRODUCTION simply pass through that state

        if ns_state != State.PRODUCTION:
            return ns_state

        # if physical interface state is connected
        # return PRODUCTION state

        if phy_state == 1:
            # connected
            return State.PRODUCTION

        # otherwise return ALLOCATED state for now
        #TODO: better mapping
        """
        1 = CONNECTED
        2 = DISABLED
        3 = NOT CONNECTED
        4 = AWAITING X-CONNECT
        5 = QUARANTINE
        """

        return State.ALLOCATED

    @property
    def status(self):
        return []

    @property
    def managing_account(self):
        # should this be the ix or the network?
        return self._customer.id

    @property
    def consuming_account(self):
        return self._customer.id

    @property
    def billing_account(self):
        # doesn't look like ixp manager separates
        # billing accounts from customer accounts
        return self._customer.id

    @property
    def listed(self):
        # TODO: how is this determined?
        return True

    @property
    def external_ref(self):
        return f"vlaninterface:{self._customer.autsys}:{self.pk}"

    @property
    def type(self):
        return "exchange_lan"

    @property
    def network_service(self):
        return self._network_service.id

    @property
    def connection(self):
        return self._connection.id

    @property
    def role_assignments(self):
        return []

    @property
    def network_feature_configs(self):
        return []

    @property
    def vlan_config(self):
        return Dot1QVLanConfig.objects.get(id=self.vlanid.id)

    @property
    def asns(self):
        return [self._customer.autsys]

    @property
    def ip_addresses(self):
        # todo - check vlaninterface.ipvXenabled?

        ips = []

        if self.ipv4addressid:
            ips.extend(ipam_models.IpAddress.objects.filter(
                address=self.ipv4addressid.address
            ))

        if self.ipv6addressid:
            ips.extend(ipam_models.IpAddress.objects.filter(
                address=self.ipv6addressid.address
            ))

        return ips

    @property
    def mac_addresses(self):
        return ipam_models.MacAddress.objects.filter(vlan_interface=self)



class DemarcationPoint(models.Model):
    pass


class PortVLanConfig(models.Model):
    pass



class QinQVLanConfig(models.Model):
    pass


class Dot1QVLanConfig(ixpmgr_models.Vlan):
    class Meta:
        proxy = True

    proxies = ProxyManager()
    Source = ixpmgr_models.Vlan

    vlan = ProxyField(Source.id)


    vlan_ethertype = NullField()

    @property
    def vlan_type(self):
        return "dot1q"




class NetworkServiceConfig(models.Model):
    pass

class P2PNetworkServiceConfig(models.Model):
    pass


class MP2MPNetworkServiceConfig(models.Model):
    pass


class P2MPNetworkServiceConfig(models.Model):
    pass


class CloudNetworkServiceConfig(models.Model):
    pass



class BlackholingNetworkFeatureConfig(models.Model):
    pass


class RouteServerNetworkFeatureConfig(models.Model):
    pass


class IXPRouterNetworkFeatureConfig(models.Model):
    pass
