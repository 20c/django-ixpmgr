from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *

class Connection(ixpmgr_models.Physicalinterface):
    proxies = ProxyManager()
    class Meta:
        proxy = True

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
    id = NullField()
    name = NullField()
    ports = NullField()
    vlan_types = NullField()
    outer_vlan_ethertypes = NullField()

class ExchangeLanNetworkServiceConfig(ixpmgr_models.Vlaninterface):
    proxies = ProxyManager()
    Source = ixpmgr_models.Vlaninterface
    class Meta:
        proxy = True

    network_service = NullField()
    @property
    def type(self):
        return ""

    @property
    def network_service(self):
        return ""

    """
"type": "exchange_lan",
"state": "requested",
"status": [],
"id": "string",
"network_service": "string",
"managing_account": "238189294",
"consuming_account": "2381982",
"external_ref": "IX:Service:23042",
"purchase_order": "Project: DC Moon",
"contract_ref": "contract:31824",
"billing_account": "string",
"role_assignments": [],
"connection": "string",
"network_feature_configs": [],
"vlan_config": {},
"capacity": 1,
"asns": [],
"macs": [],
"ips": [],
"listed": true
    """


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
