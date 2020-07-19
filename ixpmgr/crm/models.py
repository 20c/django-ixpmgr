from django.db import models
import django_ixpmgr.models as ixpmodels
from django_ixpmgr.model_util import ProxyModel, ProxyField, ProxyManager

def join_address(*parts):
    return '\n'.join(p for p in parts if p) or None


class RegAddress(ProxyModel, ixpmodels.CompanyRegistrationDetail):
    class Meta: proxy = True
    Source = ixpmodels.CompanyRegistrationDetail

    locality = ProxyField(Source.towncity) # max_length=40,
    region = ProxyField(Source.jurisdiction)
    postal_code = ProxyField(Source.postcode)

    @property
    def street_address(self):
        return join_address(self.address1, self.address2, self.address3)

    @property
    def post_office_box_number(self):
        return None

class BillingInformation(ProxyModel, ixpmodels.CompanyBillingDetail):
    class Meta: proxy = True
    Source = ixpmodels.CompanyBillingDetail

    name = ProxyField(Source.billingcontactname)
    vat_number = ProxyField(Source.vatnumber)

    @property
    def address(self): return self

    country = ProxyField(Source.billingcountry) # max=2
    locality = ProxyField(Source.billingtowncity)
    # region = ProxyField(Source.jurisdiction)
    postal_code = ProxyField(Source.billingpostcode)

    @property
    def street_address(self):
        return join_address(self.billingaddress1,
                            self.billingaddress2,
                            self.billingaddress3)
    @property
    def post_office_box_number(self):
        return None

    def save(self, *a, **k):
        self.purchaseorderrequired = False
        super(BillingInformation, self).save(*a, **k)

class Account(ProxyModel, ixpmodels.Cust):
    class Meta: proxy = True
    Source = ixpmodels.Cust

    address = ProxyField(Source.company_registered_detail, proxy_model=RegAddress)
    billing_information = ProxyField(Source.company_billing_details, proxy_model=BillingInformation)

    #todo
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

    def save(self, *a, **k):
        # Required
        self.isreseller = 0
        self.in_manrs = 0
        self.in_peeringdb = 0
        self.peeringdb_oauth = 0
        super(Account, self).save(*a, **k)

class Contact(ProxyModel, ixpmodels.Contact):
    class Meta: proxy = True
    pass

class Role(models.Model): pass
