from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *

class NetworkServiceConfig(models.Model):
    type = NullField()
    network_service = NullField()


class DemarcationPoint(models.Model):
    pass


class PortVLanConfig(models.Model):
    pass


class Connection(models.Model):
    pass


class QinQVLanConfig(models.Model):
    pass


class Dot1QVLanConfig(models.Model):
    pass


class ExchangeLanNetworkServiceConfig(models.Model):
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
