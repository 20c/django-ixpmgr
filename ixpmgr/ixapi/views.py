from django.shortcuts import render
from django.apps import apps
from rest_framework.viewsets import ModelViewSet

from django_ixpmgr.model_util import chain_querysets
from . import serializers
from . import models

# View dispatching to any model mapped in the serializer class
class PolymorphicViewSet(ModelViewSet):
    def get_queryset(self):
        # assert isinstance(self.serializer_class, serializers.PolymorphicSerializer)
        return chain_querysets(
            model.objects.all() for model in self.serializer_class.model_serializer_mapping
        )


class AccountViewSet(ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class FacilityViewSet(ModelViewSet):
    queryset = models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer

class MemberJoiningRuleViewSet(PolymorphicViewSet):
    serializer_class = serializers.MemberJoiningRuleSerializer

class NetworkServiceViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkServiceSerializer
