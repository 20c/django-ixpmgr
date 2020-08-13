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

    status = NullField()
    managing_account = NullField()
    consuming_account = NullField()
    billing_account = NullField()
    external_ref = NullField()
    purchase_order = NullField()
    contract_ref = NullField()
    vlan_config = NullField()
    capacity = NullField()

    @property
    def _customer(self):
        return self.virtualinterfaceid.custid

    @property
    def _connection(self):
        return Connection.objects.get(id=self.virtualinterfaceid.id)

    @property
    def _physical(self):
        return ixpmgr_models.Physicalinterface.objects.get(
            virtualinterfaceid=self.virtualinterfaceid
        )

    @property
    def state(self):
        State = schema_entities.events.State
        ns_state = self._network_service.state
        phy_state = self._physical.status

        if ns_state != State.PRODUCTION:
            return ns_state

        if phy_state == 1:
            # connected
            return State.PRODUCTION


        #TODO: better mapping?
        """
        1 = CONNECTED
        2 = DISABLED
        3 = NOT CONNECTED
        4 = AWAITING
        5 = QUARANTINE
        """

        return State.ALLOCATED

    @property
    def managing_account(self):
        return self._customer.id

    @property
    def consuming_account(self):
        return self._customer.id

    @property
    def billing_account(self):
        return self._customer.id

    @property
    def listed(self):
        return True

    @property
    def type(self):
        return ""

    @property
    def _network_service(self):
        return service_models.ExchangeLanNetworkService.objects.get(id=self.vlanid.infrastructureid.id)

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
    def asns(self):
        return []

    @property
    def ip_addresses(self):
        # todo - check vlaninterface.ipvXenabled?
        # todo - exclude vlan.private>0 ?

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


class Dot1QVLanConfig(models.Model):
    pass


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
