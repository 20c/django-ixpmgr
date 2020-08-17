from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyField, ProxyManager, NullField

from django.conf import settings


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

        # Assumption for now, the org running ixp manager is the
        # owning org, return dummy value for now

        return getattr(
            settings,
            "IXPMANAGER_OPERATOR_NAME"
        ) or "Not specified"


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
