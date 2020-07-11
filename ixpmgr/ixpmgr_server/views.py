from django.shortcuts import render
from django.apps import apps
from rest_framework import viewsets

from . import serializers
from . import models

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()
