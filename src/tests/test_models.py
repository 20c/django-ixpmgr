import pytest
from pprint import pprint
from itertools import chain

from django.conf import settings

import crm.models
import catalog.models
import service.models
import ipam.models
import config.models
from ixapi_schema.v2.constants import (
    config as config_const, ipam as ipam_const
)



# Helpers 
def assertEqual(a,b, *args):
    assert a == b
    if args:
        for arg in args:
            assert a == arg

def get_ip_addresses(instance):
    ipv4 = []
    for vlan in instance.vlan_set.all():
        addrs = ipam.models.IpAddress.objects.filter(vlanid=vlan.id)
        ipv4.extend(addrs)
    return ipv4

# ------- CRM tests ----------
@pytest.mark.django_db
def test_reg_address(ixpmgr_data, ixpmgr_models):
    _id = 1
    regaddress = crm.models.RegAddress.objects.get(id=_id)
    company_reg_detail = ixpmgr_models.CompanyRegistrationDetail.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.companyregistrationdetail"][_id]

    assertEqual(regaddress.locality, company_reg_detail.towncity, expected["towncity"])
    assertEqual(regaddress.region, company_reg_detail.jurisdiction, None)
    assertEqual(regaddress.postal_code, company_reg_detail.postcode, expected["postcode"])
    assertEqual(regaddress.street_address, company_reg_detail.address1, expected["address1"])
    assertEqual(regaddress.post_office_box_number, None)


@pytest.mark.django_db
def test_billing_information(ixpmgr_data, ixpmgr_models):
    _id = 1
    billing_information = crm.models.BillingInformation.objects.get(id=_id)
    company_billing_detail = ixpmgr_models.CompanyBillingDetail.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.companybillingdetail"][_id]

    assertEqual(
        billing_information.name,
        company_billing_detail.billingcontactname,
        expected["billingcontactname"])
    assertEqual(
        billing_information.vat_number,
        company_billing_detail.vatnumber,
        expected["vatnumber"])
    assertEqual(billing_information.address, billing_information)
    assertEqual(billing_information.country, company_billing_detail.billingcountry, expected["billingcountry"])
    assertEqual(billing_information.locality, company_billing_detail.billingtowncity, expected["billingtowncity"])    
    assertEqual(billing_information.postal_code, company_billing_detail.billingpostcode, expected["billingpostcode"])    
    assertEqual(billing_information.street_address, company_billing_detail.billingaddress1, expected["billingaddress1"])    
    assertEqual(billing_information.post_office_box_number, None)
    assertEqual(billing_information.purchaseorderrequired, False)


@pytest.mark.django_db
def test_account(ixpmgr_data, ixpmgr_models):
    _id = 1
    account = crm.models.Account.objects.get(id=_id)
    cust = ixpmgr_models.Cust.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.cust"][_id]

    assertEqual(account.address.pk, cust.company_registered_detail.pk, expected["company_registered_detail"])
    assertEqual(account.billing_information.pk, cust.company_billing_details.pk, expected["company_billing_details"])
    assertEqual(account.managing_account, account.id)
    assertEqual(account.legal_name, account.address.registeredname)
    assertEqual(account.external_ref, f"cust:{account.id}")
    assertEqual(account.discoverable, True)
    assertEqual(account.isreseller, 0)
    assertEqual(account.in_manrs, 0)
    assertEqual(account.in_peeringdb, 0)
    assertEqual(account.peeringdb_oauth, 1)


# ------- Catalog tests ----------
@pytest.mark.django_db
def test_facility(ixpmgr_data, ixpmgr_models):
    _id = 1
    facility = catalog.models.Facility.objects.get(id=_id)
    location = ixpmgr_models.Location.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.location"][_id]

    assertEqual(facility.metro_area, location.city, expected["city"])
    assertEqual(facility.address_country, location.country, expected["country"])
    assertEqual(facility.address_locality, location.city, expected["city"])
    assertEqual(facility.address_region, None)
    assertEqual(facility.postal_code, None)
    assertEqual(facility.street_address, location.address, expected["address"])
    assertEqual(facility.peeringdb_facility_id, location.pdb_facility_id, expected["pdb_facility_id"])
    assertEqual(facility.cluster, None)
    assertEqual(facility.operator_name, "Not specified")

@pytest.mark.django_db
def test_device(ixpmgr_data, ixpmgr_models):
    _id = 1
    device = catalog.models.Device.objects.get(id=_id)
    switch = ixpmgr_models.Switch.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.switch"][_id]

    assertEqual(device.pop, None)
    assertEqual(device.capabilities, None)
    assertEqual(device.facility, catalog.models.Facility.objects.get(id=device.infrastructure.id))


# ------- Service tests ----------
@pytest.mark.django_db
def test_allow_member_joining_rule(ixpmgr_data, ixpmgr_models):
    _id = 1
    amjr = service.models.AllowMemberJoiningRule.objects.get(id=_id)
    cust = ixpmgr_models.Cust.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.cust"][_id]

    assertEqual(amjr.managing_account, None)
    assertEqual(amjr.consuming_account, None)
    assertEqual(amjr.network_service, None)
    assertEqual(amjr.test_cust_name, cust.name, expected["name"])
    assertEqual(amjr.capacity_min, None)
    assertEqual(amjr.capacity_max, None)

@pytest.mark.django_db
def test_exchange_lan_network_service(ixpmgr_data, ixpmgr_models):
    _id = 1
    elns = service.models.ExchangeLanNetworkService.objects.get(id=_id)
    infra = ixpmgr_models.Infrastructure.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.infrastructure"][_id]

    assertEqual(elns.external_ref, None)
    assertEqual(elns.metro_area, "IDK")
    assertEqual(elns.product_offering, None)
    assertEqual(elns.all_nsc_required_contact_roles, None)
    assertEqual(elns.peeringdb_ixid, infra.peeringdb_ix_id, expected["peeringdb_ix_id"])
    assertEqual(elns.ixfdb_ixid, infra.ixf_ix_id, expected["ixf_ix_id"])
    assertEqual(elns.status, None)

    customer = ixpmgr_models.CustomerToIxp.objects.filter(ixp=elns.ixp).first().customer
    state = customer.status
    qsets = (
            service.models.RouteServerNetworkFeature.objects.filter(vlan=vlan).all()
            for vlan in elns.vlan_set.all()
            )
    network_features = list(chain(*qsets))

    assertEqual(elns.network_features, network_features)
    assertEqual(elns.managing_account, customer.id)
    assertEqual(elns.consuming_account, customer.id)
    assertEqual(elns.type, "exchange_lan")
    #FIXME
    # import not working
    # assertEqual(elns.state, None)
    ipv4 = get_ip_addresses(elns)
    assertEqual(elns.ip_addresses, ipv4)
    assertEqual(elns.isprimary, True)

@pytest.mark.django_db
def test_route_server_network_feature(ixpmgr_data, ixpmgr_models):
    _id = 1
    rsnf = service.models.RouteServerNetworkFeature.objects.get(id=_id)
    infra = ixpmgr_models.Infrastructure.objects.get(id=_id)
    expected = ixpmgr_data["ixpmgr.infrastructure"][_id]

    assertEqual(rsnf.fqdn, "example.com")
    assertEqual(rsnf.required, False)
    assertEqual(rsnf.all_nfc_required_contact_roles, None)
    assertEqual(rsnf.ixp_specific_flags, [])

    assertEqual(rsnf.network_service, service.models.ExchangeLanNetworkService.objects.get(vlan=rsnf.vlan))
    assertEqual(rsnf.looking_glass_url, "https://lg.moon-ix.net/rs1")

    assertEqual(rsnf.address_families, [ipam_const.AddressFamilies.AF_INET])
    # assertEqual(rsnf.session_mode, config_const.RouteServerSessionMode.MODE_PUBLIC)
    assertEqual(rsnf.available_bgp_session_types, None)

    #FIXME property isn't working on RouteServerNetworkFeature
    # ipv4 = get_ip_addresses(rsnf)
    # assertEqual(rsnf.ip_addresses, ipv4)

# ------- IPAM tests ----------
