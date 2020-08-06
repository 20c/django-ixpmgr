# serializers.py
from rest_framework import serializers
# ModelSerializer = serializers.ModelSerializer
ModelSerializer = serializers.HyperlinkedModelSerializer

import ixapi_schema.v2.schema as ixser
from . import models

# Pattern ripped from django-rest-polymorphic
# Simple dispatch, child classes just define a mapping of model class => serializer class
class PolymorphicSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(PolymorphicSerializer, self).__init__(*args, **kwargs)

        # Overwrite mapped serializer classes with instances
        model_serializer_mapping = self.model_serializer_mapping
        self.model_serializer_mapping = {}
        for model, serializer in model_serializer_mapping.items():
            if callable(serializer):
                serializer = serializer(*args, **kwargs)
            self.model_serializer_mapping[model] = serializer

    def to_representation(self, instance):
        seri = self.model_serializer_mapping[instance.__class__]
        ret = seri.to_representation(instance)
        # todo: set "type" to serializer.__polymorphic_type__?
        return ret


class AccountSerializer(ixser.Account, ModelSerializer):
    class Meta:
        many = True
        model = models.Account
        fields = [
            "id",
            "name",
            "address",
            "managing_account",
            "legal_name",
            "billing_information",
            "external_ref",
            "discoverable",
        ]


class FacilitySerializer(ixser.Facility, ModelSerializer):
    class Meta:
        many = True
        model = models.Facility
        fields = [
            "id",
            "name",
            "metro_area",
            "address_country",
            "address_locality",
            "address_region",
            "postal_code",
            "street_address",
            "peeringdb_facility_id",
            "organisation_name",
            "cluster",
        ]

# Member list

class DenyMemberJoiningRuleSerializer(ixser.DenyMemberJoiningRule, ModelSerializer):
    class Meta:
        many = True
        model = models.DenyMemberJoiningRule
        fields = [
            "id",
            "managing_account",
            "consuming_account",
            "id",
            "network_service",
            "type",
        ]

class AllowMemberJoiningRuleSerializer(ixser.AllowMemberJoiningRule, ModelSerializer):
    class Meta:
        many = True
        model = models.AllowMemberJoiningRule
        fields = [
            "id",
            "managing_account",
            "consuming_account",
            "capacity_min",
            "capacity_max",
            "network_service",
            "type",
            "test_cust_name",
        ]

class MemberJoiningRuleSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.AllowMemberJoiningRule: AllowMemberJoiningRuleSerializer,
        models.DenyMemberJoiningRule: DenyMemberJoiningRuleSerializer,
    }


# Network services

class ExchangeLanNetworkServiceSerializer(ixser.ExchangeLanNetworkService, ModelSerializer):
    class Meta:
        many = True
        model = models.ExchangeLanNetworkService
        fields = [
            "id",
            "managing_account",
            "consuming_account",
            "product_offering",
            "name",
            "metro_area",
            "nsc_required_contact_roles",
            "network_features",
            "ips",
            "peeringdb_ixid",
            "ixfdb_ixid",
            "state",
            "status",
            "type",
        ]

class P2PNetworkServiceSerializer(ixser.P2PNetworkService, ModelSerializer):
    class Meta:
        many = True
        model = models.P2PNetworkService
        fields = (
            "joining_member_account",
            "capacity",
            "nsc_required_contact_roles",
            "contract_ref",
            "external_ref",
            "purchase_order",
            "type",
        )

class P2MPNetworkServiceSerializer(ixser.P2MPNetworkService, ModelSerializer):
    class Meta:
        many = True
        model = models.P2MPNetworkService
        fields = (
            "name",
            "billing_account",
            "initiator_capacity",
            "default_capacity_min",
            "default_capacity_max",
            "nsc_required_contact_roles",
            "network_features",
            "member_joining_rules",
            "type",
        )

class MP2MPNetworkServiceSerializer(ixser.MP2MPNetworkService, ModelSerializer):
    class Meta:
        many = True
        model = models.MP2MPNetworkService
        fields = (
            "name",
            "billing_account",
            "initiator_capacity",
            "default_capacity_min",
            "default_capacity_max",
            "nsc_required_contact_roles",
            "member_joining_rules",
            "network_features",
            "type",
        )

class CloudNetworkServiceSerializer(ixser.CloudNetworkService, ModelSerializer):
    class Meta:
        many = True
        model = models.CloudNetworkService
        fields = (
            "billing_account",
            "cloud_key",
            "diversity",
            "type",
        )

class NetworkServiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.ExchangeLanNetworkService: ExchangeLanNetworkServiceSerializer,
#        models.P2PNetworkService: P2PNetworkServiceSerializer,
#        models.P2MPNetworkService: P2MPNetworkServiceSerializer,
#        models.MP2MPNetworkService: MP2MPNetworkServiceSerializer,
#        models.CloudNetworkService: CloudNetworkServiceSerializer,
    }
