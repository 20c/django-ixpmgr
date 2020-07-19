from django.db import models
import django_ixpmgr.models as ixpmodels
from django_ixpmgr.model_util import ProxyModel, ProxyField, ProxyManager, NullField

class Facility(ProxyModel, ixpmodels.Location):
    class Meta:
        proxy = True
    Source = ixpmodels.Location

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
        cabinet = ixpmodels.Cabinet.objects.get(locationid=self.id)
        q = ixpmodels.Custkit.objects.filter(cabinetid=cabinet.id)
        cust = q.first().custid
        return cust.name


class Device(models.Model):
    "name",
    "capabilities",
    "physical_facility",

class ProductOffering(models.Model): pass
class PointOfPresence(models.Model): pass
class ExchangeLanNetworkProductOffering(models.Model): pass
class CloudNetworkProductOffering(models.Model): pass
class P2PNetworkProductOffering(models.Model): pass
class P2MPNetworkProductOffering(models.Model): pass
class MP2MPNetworkProductOffering(models.Model): pass
