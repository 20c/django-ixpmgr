from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyManager


class Facility(ixpmgr_models.Location):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.Location

    metro_area            = proxies.field(Source.city)
    address_country       = proxies.field(Source.country)
    address_locality      = proxies.field(Source.city)
    address_region        = proxies.null_field()
    postal_code           = proxies.null_field()
    street_address        = proxies.field(Source.address)
    peeringdb_facility_id = proxies.field(Source.pdb_facility_id)
    cluster               = proxies.null_field()

    @property
    def operator_name(self):
        return "Some Org"

        # TODO: i don't think this is right for the operator / org
        # name, it reads off of the colocation equipment table
        # and there can be multiple customers in there
        #
        # Assumption for now, the org running ixp manager is the
        # owning org, return dummy value for now

        cabinet = ixpmgr_models.Cabinet.objects.get(locationid=self.id)
        q = ixpmgr_models.Custkit.objects.filter(cabinetid=cabinet.id)
        if q.exists():
            cust = q.first().custid
            return cust.name
        else:
            return None


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
