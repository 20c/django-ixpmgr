from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyField, ProxyManager, NullField


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


class Device(ixpmgr_models.Switch):

    """
    A Device is a network hardware device, typically a switch, which is located at a specified facility and inside a PointOfPresence. PoPs.

    They may be physically located at their related PoPs.

    Currently implemented in it's most basic form so we can reference it
    in `Port`
    """

    class Meta:
        proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.Switch

    # unmapped

    pop = NullField()
    capabilities = NullField()

    # mapped as is
    # - name

    # direct mapped

    # indirect mapped

    @property
    def facility(self):
        return Facility.objects.get(id=self.infrastructure.id)


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
