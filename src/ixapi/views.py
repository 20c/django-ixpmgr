from django.shortcuts import render
from django.apps import apps
from rest_framework import viewsets, mixins

from django_ixpmgr.model_util import chain_querysets
from . import serializers, models

# Default to read-only views
_BaseViewSet = viewsets.ReadOnlyModelViewSet

# View dispatching to any model mapped in the serializer class
class PolymorphicViewSet(_BaseViewSet):

    # class property that allows to set filters
    # for the get_queryset operation, leaving it
    # empty is identical to all()
    queryset_filters = {}

    def get_queryset(self):
        # assert isinstance(self.serializer_class, serializers.PolymorphicSerializer)
        return chain_querysets(
            model.objects.filter(**self.queryset_filters)
            for model in self.serializer_class.model_serializer_mapping
        )

class PutableViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet): pass


class AccountViewSet(_BaseViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class FacilityViewSet(_BaseViewSet):
    queryset = models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer

class IpAddressViewSet(_BaseViewSet):
    lookup_value_regex = "[0-9.:]+"
    lookup_field = "address"
    queryset = models.IpAddress.objects.all()
    serializer_class = serializers.IpAddressSerializer

    def get_object(self):
        return models.IpAddress.objects.get(**self.kwargs)


# mac address is PUTable
class MacAddressViewSet(PutableViewSet):
    queryset = models.MacAddress.objects.all()
    serializer_class = serializers.MacAddressSerializer

class ConnectionViewSet(_BaseViewSet):
    queryset = models.Connection.objects.all()
    serializer_class = serializers.ConnectionSerializer

class MemberJoiningRuleViewSet(PolymorphicViewSet):
    serializer_class = serializers.MemberJoiningRuleSerializer

class NetworkServiceViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkServiceSerializer

class NetworkFeatureViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkFeatureSerializer

class NetworkServiceConfigViewSet(PolymorphicViewSet):
    #TODO: this contain private vlans?
    serializer_class = serializers.NetworkServiceConfigSerializer
