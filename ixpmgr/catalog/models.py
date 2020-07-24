from django.db import models
import django_ixpmgr.models as ixpmgr_models
from django_ixpmgr.model_util import *


class Facility(ixpmgr_models.Location):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.Location

    metro_area = ProxyField(Source.city)
    address_country = ProxyField(Source.country)
    address_locality = ProxyField(Source.city)
    address_region = NullField()
    postal_code = NullField()
    street_address = ProxyField(Source.address)
    peeringdb_facility_id = ProxyField(Source.pdb_facility_id)
    cluster = NullField()

    @property
    def operator_name(self):
        cabinet = ixpmgr_models.Cabinet.objects.get(locationid=self.id)
        q = ixpmgr_models.Custkit.objects.filter(cabinetid=cabinet.id)
        cust = q.first().custid
        return cust.name


class Device(models.Model):
    pass


class ProductOffering(models.Model):
    pass


class PointOfPresence(models.Model):
    pass


class ExchangeLanNetworkProductOffering(models.Model):
    pass


class CloudNetworkProductOffering(models.Model):
    pass


class P2PNetworkProductOffering(models.Model):
    pass


class P2MPNetworkProductOffering(models.Model):
    pass


class MP2MPNetworkProductOffering(models.Model):
    pass
