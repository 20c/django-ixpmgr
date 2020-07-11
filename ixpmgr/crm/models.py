from django.db import models
import django_ixpmgr.models as ixpmgr_models

class Account(models.Model):
    source = models.OneToOneField(ixpmgr_models.Cust, models.CASCADE, primary_key=True)

    # replace with field aliases? https://shezadkhan.com/aliasing-fields-in-django/
    id = models.CharField(max_length=80)
    name = models.CharField(max_length=80) # but source name max=255
    address = models.ForeignKey("crm.Address", models.DO_NOTHING)

    managing_account = models.ForeignKey("self", models.DO_NOTHING, null=True)
    legal_name = models.CharField(max_length=80, null=True)
    billing_information = models.ForeignKey("crm.BillingInformation", models.DO_NOTHING, null=True)
    external_ref = models.CharField(max_length=80, null=True)
    discoverable = models.BooleanField()

class Address(models.Model):
    source = models.OneToOneField(ixpmgr_models.CompanyRegistrationDetail, models.CASCADE, primary_key=True)

class BillingInformation(models.Model):
    source = models.OneToOneField(ixpmgr_models.CompanyBillingDetail, models.CASCADE, primary_key=True)

class Contact(models.Model):
    source = models.OneToOneField(ixpmgr_models.Contact, models.CASCADE, primary_key=True)

class Role(models.Model): pass
