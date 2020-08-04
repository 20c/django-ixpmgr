from django.db import models
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyField, ProxyManager


def join_address(*parts):
    return "\n".join(p for p in parts if p) or None


class RegAddress(ixpmgr_models.CompanyRegistrationDetail):
    proxies = ProxyManager()
    class Meta:
        proxy = True

    Source = ixpmgr_models.CompanyRegistrationDetail

    locality = ProxyField(Source.towncity)  # max_length=40,
    region = ProxyField(Source.jurisdiction)
    postal_code = ProxyField(Source.postcode)

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

    name = ProxyField(Source.billingcontactname)
    vat_number = ProxyField(Source.vatnumber)

    @property
    def address(self):
        return self

    country = ProxyField(Source.billingcountry)  # max=2
    locality = ProxyField(Source.billingtowncity)
    postal_code = ProxyField(Source.billingpostcode)

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
    address = ProxyField(Source.company_registered_detail, proxy_model=RegAddress)
    billing_information = ProxyField(
        Source.company_billing_details, proxy_model=BillingInformation
    )

    @property
    def managing_account(self):
        pass

    @property
    def legal_name(self):
        pass

    @property
    def external_ref(self):
        pass

    @property
    def discoverable(self):
        pass

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


class Role(models.Model):
    pass
