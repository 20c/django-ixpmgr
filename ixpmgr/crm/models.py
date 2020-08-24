from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import *


def join_address(*parts):
    return "\n".join(p for p in parts if p) or None


class RegAddress(ixpmgr_models.CompanyRegistrationDetail):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.CompanyRegistrationDetail

    locality = proxies.field(Source.towncity)  # max_length=40,
    region = proxies.field(Source.jurisdiction)
    postal_code = proxies.field(Source.postcode)

    @property
    def street_address(self):
        return join_address(self.address1, self.address2, self.address3)

    @property
    def post_office_box_number(self):
        return None


class BillingInformation(ixpmgr_models.CompanyBillingDetail):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.CompanyBillingDetail

    name = proxies.field(Source.billingcontactname)
    vat_number = proxies.field(Source.vatnumber)

    @property
    def address(self):
        return self

    country = proxies.field(Source.billingcountry)  # max=2
    locality = proxies.field(Source.billingtowncity)
    postal_code = proxies.field(Source.billingpostcode)

    @property
    def street_address(self):
        return join_address(
            self.billingaddress1, self.billingaddress2, self.billingaddress3
        )

    @property
    def post_office_box_number(self):
        return None

    def save(self, *args, **kwargs):
        self.purchaseorderrequired = False
        super().save(*args, **kwargs)


class Account(ixpmgr_models.Cust):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.Cust

    # name => shortname?
    address = proxies.field(Source.company_registered_detail, proxy_model=RegAddress)
    billing_information = proxies.field(
        Source.company_billing_details, proxy_model=BillingInformation
    )

    @property
    def managing_account(self):
        # TODO: what is the managing account in the context
        # of an ixp manager customer account ? itself?
        return self.id

    @property
    def legal_name(self):
        return self.address.registeredname

    @property
    def external_ref(self):
        return f"cust:{self.id}"

    discoverable = proxies.const_field(True)

    def save(self, *args, **kwargs):
        # Required
        self.isreseller = 0
        self.in_manrs = 0
        self.in_peeringdb = 0
        self.peeringdb_oauth = 0
        super().save(*args, **kwargs)


class Contact(ixpmgr_models.Contact):
    proxies = ProxyManager()
    class Meta:
        proxy = True


class Role(models.Model): pass
class RoleAssignment(models.Model): pass
