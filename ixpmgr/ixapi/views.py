from django.shortcuts import render
from django.apps import apps
from rest_framework.viewsets import ModelViewSet

from django_ixpmgr.model_util import chain_querysets
from . import serializers, models


# View dispatching to any model mapped in the serializer class
class PolymorphicViewSet(ModelViewSet):

    # class property that allows to set filters
    # for the get_queryset operation, leaving it
    # empty is identical to all()
    queryset_filters = {}

    def get_queryset(self):
        # assert isinstance(self.serializer_class, serializers.PolymorphicSerializer)
        return chain_querysets(
            model.objects.filter(**self.queryset_filters) for model in self.serializer_class.model_serializer_mapping
        )


class AccountViewSet(ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class FacilityViewSet(ModelViewSet):
    queryset = models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer

class IpAddressViewSet(ModelViewSet):
    queryset = models.IpAddress.objects.all()
    serializer_class = serializers.IpAddressSerializer

class MacAddressViewSet(ModelViewSet):
    queryset = models.MacAddress.objects.all()
    serializer_class = serializers.MacAddressSerializer

class MemberJoiningRuleViewSet(PolymorphicViewSet):
    serializer_class = serializers.MemberJoiningRuleSerializer

class NetworkServiceViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkServiceSerializer

class NetworkFeatureViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkFeatureSerializer

class NetworkServiceConfigViewSet(PolymorphicViewSet):
    #TODO: should this contain private vlans?
    serializer_class = serializers.NetworkServiceConfigSerializer
