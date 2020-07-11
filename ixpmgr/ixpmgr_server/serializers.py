from rest_framework import serializers

import ixapi_schema.v2.schema as ixser
from . import models


class AccountSerializer(ixser.Account, serializers.ModelSerializer):
    is_reseller = serializers.IntegerField(source='isreseller')
    in_manrs = serializers.IntegerField()
    in_peeringdb = serializers.IntegerField()
    peeringdb_oauth = serializers.IntegerField()

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

            'is_reseller',
            'in_manrs',
            'in_peeringdb',
            'peeringdb_oauth',
        ]
