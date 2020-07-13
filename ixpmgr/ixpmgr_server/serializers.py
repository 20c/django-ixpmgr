from rest_framework import serializers

import ixapi_schema.v2.schema as ixser
from . import models


class AccountSerializer(ixser.Account, serializers.ModelSerializer):
    class Meta:
        many = True
        model = models.Account
        fields = [
            'name',
            'address',
            'managing_account',
            'legal_name',
            'billing_information',
            'external_ref',
            'discoverable',
        ]
