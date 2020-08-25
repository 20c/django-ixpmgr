import pytest
from pprint import pprint
import crm.models
import catalog.models
import service.models
import ipam.models
import config.models

# Helpers 
def assertEqual(a,b, *args):
    assert a == b
    if args:
        for arg in args:
            assert a == arg

# CRM tests
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


# Catalog tests



