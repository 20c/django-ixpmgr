from itertools import chain

from django.shortcuts import render
from django.apps import apps
from rest_framework import viewsets

from . import serializers
from . import models

# View dispatching to any model mapped in the serializer class
class PolymorphicViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # assert isinstance(self.serializer_class, serializers.PolymorphicSerializer)
        model_serializers = self.serializer_class.model_serializer_mapping
        querysets = {
            model: model.objects.all() for model in model_serializers
        }
        return list(chain(*querysets.values()))


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = models.Facility.objects.all()
    serializer_class = serializers.FacilitySerializer

class MemberJoiningRuleViewSet(PolymorphicViewSet):
    serializer_class = serializers.MemberJoiningRuleSerializer

class NetworkServiceViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkServiceSerializer
