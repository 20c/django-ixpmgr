
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField


class ApiKeys(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('User')
    api_key = models.CharField(db_column='apiKey', unique=True, max_length=255)
    expires = models.DateTimeField(blank=True, null=True)
    allowed_ips = models.TextField(db_column='allowedIPs', blank=True)
    created = models.DateTimeField()
    last_seen_at = models.DateTimeField(db_column='lastseenAt', blank=True, null=True)
    last_seen_from = models.CharField(db_column='lastseenFrom', max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'api_keys'


class Bgpsessiondata(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    srcipaddressid = models.IntegerField(blank=True, null=True)
    dstipaddressid = models.IntegerField(blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    vlan = models.IntegerField(blank=True, null=True)
    packetcount = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=40, blank=True)

    class Meta:
        managed = False
        db_table = 'bgpsessiondata'


class Cabinet(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    locationid = models.ForeignKey('Location', db_column='locationid', blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True)
    cololocation = models.CharField(max_length=255, blank=True)
    height = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'cabinet'


class ChangeLog(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_by = models.ForeignKey('User', db_column='created_by', blank=True, null=True)
    title = models.CharField(max_length=255)
    details = models.TextField()
    visibility = models.IntegerField()
    livedate = models.DateField()
    version = models.BigIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'change_log'


class CompanyBillingDetail(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    billingcontactname = models.CharField(db_column='billingContactName', max_length=255, blank=True)  # Field name made lowercase.
    billingaddress1 = models.CharField(db_column='billingAddress1', max_length=255, blank=True)  # Field name made lowercase.
    billingaddress2 = models.CharField(db_column='billingAddress2', max_length=255, blank=True)  # Field name made lowercase.
    billingaddress3 = models.CharField(db_column='billingAddress3', max_length=255, blank=True)  # Field name made lowercase.
    billingtowncity = models.CharField(db_column='billingTownCity', max_length=255, blank=True)  # Field name made lowercase.
    billingpostcode = models.CharField(db_column='billingPostcode', max_length=255, blank=True)  # Field name made lowercase.
    billingcountry = models.CharField(db_column='billingCountry', max_length=255, blank=True)  # Field name made lowercase.
    billingemail = models.CharField(db_column='billingEmail', max_length=255, blank=True)  # Field name made lowercase.
    billingtelephone = models.CharField(db_column='billingTelephone', max_length=255, blank=True)  # Field name made lowercase.
    vatnumber = models.CharField(db_column='vatNumber', max_length=255, blank=True)  # Field name made lowercase.
    vatrate = models.CharField(db_column='vatRate', max_length=255, blank=True)  # Field name made lowercase.
    purchase_order_required = models.BooleanField(default=False, db_column='purchaseOrderRequired')
    invoicemethod = models.CharField(db_column='invoiceMethod', max_length=255, blank=True)  # Field name made lowercase.
    invoiceemail = models.CharField(db_column='invoiceEmail', max_length=255, blank=True)  # Field name made lowercase.
    billingfrequency = models.CharField(db_column='billingFrequency', max_length=255, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_billing_detail'


class CompanyRegistrationDetail(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    registeredname = models.CharField(db_column='registeredName', max_length=255, blank=True)  # Field name made lowercase.
    companynumber = models.CharField(db_column='companyNumber', max_length=255, blank=True)  # Field name made lowercase.
    jurisdiction = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    towncity = models.CharField(db_column='townCity', max_length=255, blank=True)  # Field name made lowercase.
    postcode = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'company_registration_detail'


class Consoleserverconnection(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    customer = models.ForeignKey('Customer', db_column='custid', blank=True, null=True)
    switchid = models.ForeignKey('Switch', db_column='switchid', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    port = models.CharField(max_length=255, blank=True)
    speed = models.IntegerField(blank=True, null=True)
    parity = models.IntegerField(blank=True, null=True)
    stopbits = models.IntegerField(blank=True, null=True)
    flowcontrol = models.IntegerField(blank=True, null=True)
    autobaud = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'consoleserverconnection'


class Contact(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey('User', unique=True, blank=True, null=True)
    customer = models.ForeignKey('Customer', db_column='custid', blank=True, null=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    facilityaccess = models.IntegerField()
    mayauthorize = models.IntegerField()
    notes = models.TextField(blank=True)
    lastupdated = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=32, blank=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContactGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    active = models.IntegerField()
    limited_to = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'contact_group'


class ContactToGroup(models.Model):
    contact = models.ForeignKey(Contact)
    contact_group = models.ForeignKey(ContactGroup)

    class Meta:
        managed = False
        db_table = 'contact_to_group'


class Customer(models.Model):
    #id = models.AutoField()
    irrdb = models.ForeignKey('Irrdbconfig', db_column='irrdb', blank=True, null=True)
    company_registered_detail = models.ForeignKey(CompanyRegistrationDetail, blank=True, null=True)
    company_billing_details = models.ForeignKey(CompanyBillingDetail, blank=True, null=True)
    reseller = models.ForeignKey('self', db_column='reseller', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.IntegerField(blank=True, null=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True)
    abbreviatedname = models.CharField(db_column='abbreviatedName', max_length=30, blank=True)  # Field name made lowercase.
    autsys = models.IntegerField(blank=True, null=True)
    maxprefixes = models.IntegerField(blank=True, null=True)
    peeringemail = models.CharField(max_length=255, blank=True)
    nocphone = models.CharField(max_length=255, blank=True)
    noc24hphone = models.CharField(max_length=255, blank=True)
    nocfax = models.CharField(max_length=255, blank=True)
    nocemail = models.CharField(max_length=255, blank=True)
    nochours = models.CharField(max_length=255, blank=True)
    nocwww = models.CharField(max_length=255, blank=True)
    peeringmacro = models.CharField(max_length=255, blank=True)
    peeringmacrov6 = models.CharField(max_length=255, blank=True)
    peeringpolicy = models.CharField(max_length=255, blank=True)
    corpwww = models.CharField(max_length=255, blank=True)
    datejoin = models.DateField(blank=True, null=True)
    dateleave = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    activepeeringmatrix = models.IntegerField(blank=True, null=True)
    peeringdb = models.CharField(db_column='peeringDb', max_length=255, blank=True)  # Field name made lowercase.
    lastupdated = models.DateField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True)
    created = models.DateField(blank=True, null=True)
    md5_support = models.CharField(db_column='MD5Support', max_length=255, blank=True)  # Field name made lowercase.
    is_reseller = models.BooleanField(db_column='isReseller', default=False)

    class Meta:
        managed = False
        db_table = 'cust'

class CustomerNotes(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer)
    private = models.IntegerField()
    title = models.CharField(max_length=255)
    note = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cust_notes'


class Customerkit(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    customer = models.ForeignKey(Customer, db_column='custid', blank=True, null=True)
    cabinetid = models.ForeignKey(Cabinet, db_column='cabinetid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    descr = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'custkit'


class CustomerToIxp(models.Model):
    customer = models.ForeignKey(Customer)
    ixp = models.ForeignKey('Ixp')

    class Meta:
        managed = False
        db_table = 'customer_to_ixp'


class Infrastructure(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    ixp = models.ForeignKey('Ixp')
    name = models.CharField(max_length=255, blank=True)
    shortname = models.CharField(max_length=255, blank=True)
    isprimary = models.IntegerField(db_column='isPrimary')  # Field name made lowercase.
    aggregate_graph_name = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'infrastructure'


class Ipv4Address(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    vlan = models.ForeignKey('Vlan', db_column='vlanid', blank=True, null=True)
    address = models.CharField(max_length=16, blank=True)

    class Meta:
        managed = False
        db_table = 'ipv4address'


class Ipv6Address(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    vlan = models.ForeignKey('Vlan', db_column='vlanid', blank=True, null=True)
    address = models.CharField(max_length=40, blank=True)

    class Meta:
        managed = False
        db_table = 'ipv6address'


class IrrdbAsn(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer)
    asn = models.IntegerField()
    protocol = models.IntegerField()
    first_seen = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'irrdb_asn'


class IrrdbPrefix(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer)
    prefix = models.CharField(max_length=255)
    protocol = models.IntegerField()
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'irrdb_prefix'


class Irrdbconfig(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    host = models.CharField(max_length=255, blank=True)
    protocol = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'irrdbconfig'


class Ixp(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255, blank=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    address4 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    mrtg_path = models.CharField(max_length=255, blank=True)
    mrtg_p2p_path = models.CharField(max_length=255, blank=True)
    aggregate_graph_name = models.CharField(max_length=255, blank=True)
    smokeping = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'ixp'


class IxpmgrSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=64)
    updated = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    session_data = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'ixpmgr_session'


class Location(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255, blank=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True)
    tag = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    nocphone = models.CharField(max_length=255, blank=True)
    nocfax = models.CharField(max_length=255, blank=True)
    nocemail = models.CharField(max_length=255, blank=True)
    officephone = models.CharField(max_length=255, blank=True)
    officefax = models.CharField(max_length=255, blank=True)
    officeemail = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'location'


class MacAddress(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    virtual_interface = models.ForeignKey('VirtualInterface', related_name='mac_address_set', db_column='virtualinterfaceid', blank=True, null=True)
    firstseen = models.DateTimeField(blank=True, null=True)
    lastseen = models.DateTimeField(blank=True, null=True)
    mac = models.CharField(max_length=12, blank=True)

    class Meta:
        managed = False
        db_table = 'macaddress'


class Meeting(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created_by = models.ForeignKey('User', db_column='created_by', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    before_text = models.TextField(blank=True)
    after_text = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True)
    venue_url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting'


class MeetingItem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    meeting = models.ForeignKey(Meeting, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    company_url = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    presentation = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    video_url = models.CharField(max_length=255, blank=True)
    other_content = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting_item'


class Netinfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    vlan = models.ForeignKey('Vlan')
    protocol = models.IntegerField()
    property = models.CharField(max_length=255)
    ix = models.IntegerField()
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'netinfo'


class Networkinfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    vlan = models.ForeignKey('Vlan', db_column='vlanid', blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    network = models.CharField(max_length=255, blank=True)
    masklen = models.IntegerField(blank=True, null=True)
    rs1address = models.CharField(max_length=40, blank=True)
    rs2address = models.CharField(max_length=40, blank=True)
    dnsfile = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'networkinfo'


class Oui(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    oui = models.CharField(unique=True, max_length=6)
    organisation = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oui'


class PeeringManager(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    customer = models.ForeignKey(Customer, db_column='custid', blank=True, null=True)
    peer = models.ForeignKey(Customer, related_name='peer', db_column='peerid', blank=True, null=True)
    email_last_sent = models.DateTimeField(blank=True, null=True)
    emails_sent = models.IntegerField(blank=True, null=True)
    peered = models.IntegerField(blank=True, null=True)
    rejected = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peering_manager'


class PeeringMatrix(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    x_customer = models.ForeignKey(Customer, related_name="x_cust_id", db_column='x_custid', blank=True, null=True)
    y_customer = models.ForeignKey(Customer, related_name="y_cust_id", db_column='y_custid', blank=True, null=True)

    vlan = models.IntegerField(blank=True, null=True)
    x_as = models.IntegerField(blank=True, null=True)
    y_as = models.IntegerField(blank=True, null=True)
    peering_status = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peering_matrix'


class PhysicalInterface(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    switchport = models.ForeignKey('Switchport', related_name='physical_interface_set', db_column='switchportid', unique=True, blank=True, null=True)
    fanout_physical_interface = models.ForeignKey('self', unique=True, blank=True, null=True)
    virtual_interface = models.ForeignKey('VirtualInterface', related_name='physical_interface_set', db_column='virtualinterfaceid', blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    duplex = models.CharField(max_length=16, blank=True)
    monitorindex = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'physicalinterface'


class RsPrefixes(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    customer = models.ForeignKey(Customer, db_column='custid', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    prefix = models.CharField(max_length=64, blank=True)
    protocol = models.IntegerField(blank=True, null=True)
    irrdb = models.IntegerField(blank=True, null=True)
    rs_origin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_prefixes'


class SecEvent(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, db_column='custid', blank=True, null=True)
    switchid = models.ForeignKey('Switch', db_column='switchid', blank=True, null=True)
    switchportid = models.ForeignKey('Switchport', db_column='switchportid', blank=True, null=True)
    type = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    recorded_date = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sec_event'


class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    updated = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'session'


class Switch(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    infrastructure = models.ForeignKey(Infrastructure, db_column='infrastructure', blank=True, null=True)
    cabinetid = models.ForeignKey(Cabinet, db_column='cabinetid', blank=True, null=True)
    vendorid = models.ForeignKey('Vendor', db_column='vendorid', blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True)
    hostname = models.CharField(max_length=255, blank=True)
    ipv4addr = models.CharField(max_length=255, blank=True)
    ipv6addr = models.CharField(max_length=255, blank=True)
    snmppasswd = models.CharField(max_length=255, blank=True)
    switchtype = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=False)
    os = models.CharField(max_length=255, blank=True)
    osdate = models.DateTimeField(db_column='osDate', blank=True, null=True)  # Field name made lowercase.
    osversion = models.CharField(db_column='osVersion', max_length=255, blank=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='serialNumber', max_length=255, blank=True)  # Field name made lowercase.
    lastpolled = models.DateTimeField(db_column='lastPolled', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True)
    mausupported = models.IntegerField(db_column='mauSupported', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'switch'


class Switchport(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    switch = models.ForeignKey(Switch, db_column='switchid', blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    active = models.IntegerField()
    ifindex = models.IntegerField(db_column='ifIndex', blank=True, null=True)  # Field name made lowercase.
    ifname = models.CharField(db_column='ifName', max_length=255, blank=True)  # Field name made lowercase.
    ifalias = models.CharField(db_column='ifAlias', max_length=255, blank=True)  # Field name made lowercase.
    ifhighspeed = models.IntegerField(db_column='ifHighSpeed', blank=True, null=True)  # Field name made lowercase.
    ifmtu = models.IntegerField(db_column='ifMtu', blank=True, null=True)  # Field name made lowercase.
    ifphysaddress = models.CharField(db_column='ifPhysAddress', max_length=17, blank=True)  # Field name made lowercase.
    ifadminstatus = models.IntegerField(db_column='ifAdminStatus', blank=True, null=True)  # Field name made lowercase.
    ifoperstatus = models.IntegerField(db_column='ifOperStatus', blank=True, null=True)  # Field name made lowercase.
    iflastchange = models.IntegerField(db_column='ifLastChange', blank=True, null=True)  # Field name made lowercase.
    lastsnmppoll = models.DateTimeField(db_column='lastSnmpPoll', blank=True, null=True)  # Field name made lowercase.
    lagifindex = models.IntegerField(db_column='lagIfIndex', blank=True, null=True)  # Field name made lowercase.
    mautype = models.CharField(db_column='mauType', max_length=255, blank=True)  # Field name made lowercase.
    maustate = models.CharField(db_column='mauState', max_length=255, blank=True)  # Field name made lowercase.
    mauavailability = models.CharField(db_column='mauAvailability', max_length=255, blank=True)  # Field name made lowercase.
    maujacktype = models.CharField(db_column='mauJacktype', max_length=255, blank=True)  # Field name made lowercase.
    mauautonegsupported = models.IntegerField(db_column='mauAutoNegSupported', blank=True, null=True)  # Field name made lowercase.
    mauautonegadminstate = models.IntegerField(db_column='mauAutoNegAdminState', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'switchport'


class Traffic95Th(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    average = models.BigIntegerField(blank=True, null=True)
    max = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_95th'


class Traffic95ThMonthly(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    max_95th = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_95th_monthly'


class TrafficDaily(models.Model):
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer)
    ixp = models.ForeignKey(Ixp)
    day = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=10, blank=True)
    day_avg_in = models.BigIntegerField(blank=True, null=True)
    day_avg_out = models.BigIntegerField(blank=True, null=True)
    day_max_in = models.BigIntegerField(blank=True, null=True)
    day_max_out = models.BigIntegerField(blank=True, null=True)
    day_tot_in = models.BigIntegerField(blank=True, null=True)
    day_tot_out = models.BigIntegerField(blank=True, null=True)
    week_avg_in = models.BigIntegerField(blank=True, null=True)
    week_avg_out = models.BigIntegerField(blank=True, null=True)
    week_max_in = models.BigIntegerField(blank=True, null=True)
    week_max_out = models.BigIntegerField(blank=True, null=True)
    week_tot_in = models.BigIntegerField(blank=True, null=True)
    week_tot_out = models.BigIntegerField(blank=True, null=True)
    month_avg_in = models.BigIntegerField(blank=True, null=True)
    month_avg_out = models.BigIntegerField(blank=True, null=True)
    month_max_in = models.BigIntegerField(blank=True, null=True)
    month_max_out = models.BigIntegerField(blank=True, null=True)
    month_tot_in = models.BigIntegerField(blank=True, null=True)
    month_tot_out = models.BigIntegerField(blank=True, null=True)
    year_avg_in = models.BigIntegerField(blank=True, null=True)
    year_avg_out = models.BigIntegerField(blank=True, null=True)
    year_max_in = models.BigIntegerField(blank=True, null=True)
    year_max_out = models.BigIntegerField(blank=True, null=True)
    year_tot_in = models.BigIntegerField(blank=True, null=True)
    year_tot_out = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_daily'


class User(AbstractBaseUser, PermissionsMixin):
    ### old
    customer = models.ForeignKey(Customer, db_column='custid', blank=True, null=True)

    username = models.CharField(_('username'), max_length=255, unique=True,
        help_text=_('Required. Letters, digits and [@.+- /_=|] only.'),
        validators=[
            validators.RegexValidator(r'^[ \w.@+-=|/]+$', _('Enter a valid username.'), 'invalid')
        ])

#:    password = models.CharField(max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)

    authorised_mobile = models.CharField(db_column='authorisedMobile', max_length=30, blank=True)
    uid = models.IntegerField(blank=True, null=True)
    privs = models.IntegerField(blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)

#    is_staff = models.BooleanField(_('staff status'), default=False,
#        help_text=_('Designates whether the user can log into admin site.'))
#    is_active = models.BooleanField(_('active'), default=True,
#        help_text=_('Designates whether this user should be treated as '
#                    'active. Unselect this instead of deleting accounts.'))

    lastupdated = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)

    creator = models.CharField(max_length=255, blank=True)
    created = CreationDateTimeField(_('Created'))

#    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = False
        db_table = 'user'


    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_active(self):
        return True

    @property
    def date_joined(self):
        return created

#    @property
#    def last_login(self):
#        # FIXME - not really last login, need to join user_logins
#        return lastupdated

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.username

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


#    def last_login(self):
#        return None
#    def check_password(raw_password):
#        return False

class Vendor(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255, blank=True)
    shortname = models.CharField(max_length=255, blank=True)
    nagios_name = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'vendor'


class ViewCustCurrentActive(models.Model):
    id = models.IntegerField(primary_key=True)
    irrdb = models.IntegerField(blank=True, null=True)
    company_registered_detail_id = models.IntegerField(blank=True, null=True)
    company_billing_details_id = models.IntegerField(blank=True, null=True)
    reseller = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.IntegerField(blank=True, null=True)
    shortname = models.CharField(max_length=255, blank=True)
    abbreviatedname = models.CharField(db_column='abbreviatedName', max_length=30, blank=True)  # Field name made lowercase.
    autsys = models.IntegerField(blank=True, null=True)
    maxprefixes = models.IntegerField(blank=True, null=True)
    peeringemail = models.CharField(max_length=255, blank=True)
    nocphone = models.CharField(max_length=255, blank=True)
    noc24hphone = models.CharField(max_length=255, blank=True)
    nocfax = models.CharField(max_length=255, blank=True)
    nocemail = models.CharField(max_length=255, blank=True)
    nochours = models.CharField(max_length=255, blank=True)
    nocwww = models.CharField(max_length=255, blank=True)
    peeringmacro = models.CharField(max_length=255, blank=True)
    peeringmacrov6 = models.CharField(max_length=255, blank=True)
    peeringpolicy = models.CharField(max_length=255, blank=True)
    corpwww = models.CharField(max_length=255, blank=True)
    datejoin = models.DateField(blank=True, null=True)
    dateleave = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    activepeeringmatrix = models.IntegerField(blank=True, null=True)
    peeringdb = models.CharField(db_column='peeringDb', max_length=255, blank=True)  # Field name made lowercase.
    lastupdated = models.DateField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True)
    created = models.DateField(blank=True, null=True)
    md5support = models.CharField(db_column='MD5Support', max_length=255, blank=True)  # Field name made lowercase.
    isreseller = models.IntegerField(db_column='isReseller')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'view_cust_current_active'


class ViewSwitchDetailsByCustid(models.Model):
    id = models.IntegerField(primary_key=True)
    cust_id = models.IntegerField(blank=True, null=True, db_column='custid')
    virtualinterfaceid = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    duplex = models.CharField(max_length=16, blank=True)
    monitorindex = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    switchport = models.CharField(max_length=255, blank=True)
    switchportid = models.IntegerField()
    spifname = models.CharField(max_length=255, blank=True)
    switch = models.CharField(max_length=255, blank=True)
    switchid = models.IntegerField()
    vendorid = models.IntegerField(blank=True, null=True)
    snmppasswd = models.CharField(max_length=255, blank=True)
    infrastructure = models.IntegerField(blank=True, null=True)
    cabinet = models.CharField(max_length=255, blank=True)
    colocabinet = models.CharField(max_length=255, blank=True)
    locationname = models.CharField(max_length=255, blank=True)
    locationshortname = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'view_switch_details_by_custid'


class ViewVlanInterfaceDetailsByCustid(models.Model):
    id = models.IntegerField(primary_key=True)
    cust_id = models.IntegerField(blank=True, null=True, db_column='custid')
    virtual_interface_id = models.IntegerField(db_column='virtualinterfaceid', blank=True, null=True)
    monitorindex = models.IntegerField(blank=True, null=True)
    virtual_interface_name = models.CharField(db_column='virtualinterfacename', max_length=255, blank=True)
    vlan = models.IntegerField(blank=True, null=True)
    vlanname = models.CharField(max_length=255, blank=True)
    vlanid = models.IntegerField(blank=True, null=True)
    rcvrfname = models.CharField(max_length=255, blank=True)
    vlaninterfaceid = models.IntegerField()
    ipv4enabled = models.IntegerField(blank=True, null=True)
    ipv4hostname = models.CharField(max_length=255, blank=True)
    ipv4canping = models.IntegerField(blank=True, null=True)
    ipv4monitorrcbgp = models.IntegerField(blank=True, null=True)
    ipv6enabled = models.IntegerField(blank=True, null=True)
    ipv6hostname = models.CharField(max_length=255, blank=True)
    ipv6canping = models.IntegerField(blank=True, null=True)
    ipv6monitorrcbgp = models.IntegerField(blank=True, null=True)
    as112client = models.IntegerField(blank=True, null=True)
    mcastenabled = models.IntegerField(blank=True, null=True)
    ipv4bgpmd5secret = models.CharField(max_length=255, blank=True)
    ipv6bgpmd5secret = models.CharField(max_length=255, blank=True)
    rsclient = models.IntegerField(blank=True, null=True)
    irrdbfilter = models.IntegerField(blank=True, null=True)
    busyhost = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    ipv4address = models.CharField(max_length=16, blank=True)
    ipv6address = models.CharField(max_length=40, blank=True)

    class Meta:
        managed = False
        db_table = 'view_vlaninterface_details_by_custid'


class VirtualInterface(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    customer = models.ForeignKey(Customer, related_name='virtual_interface_set', db_column='custid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    mtu = models.IntegerField(blank=True, null=True)
    trunk = models.IntegerField(blank=True, null=True)
    channelgroup = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'virtualinterface'


class Vlan(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    infrastructureid = models.ForeignKey(Infrastructure, db_column='infrastructureid')
    name = models.CharField(max_length=255, blank=True)
    number = models.IntegerField(blank=True, null=True)
    rcvrfname = models.CharField(max_length=255, blank=True)
    private = models.IntegerField()
    notes = models.TextField(blank=True)
    peering_matrix = models.IntegerField()
    peering_manager = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vlan'


class VlanInterface(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    ipv4address = models.ForeignKey(Ipv4Address, related_name='vlan_interface_set', db_column='ipv4addressid', unique=True, blank=True, null=True)
    ipv6address = models.ForeignKey(Ipv6Address, related_name='vlan_interface_set', db_column='ipv6addressid', unique=True, blank=True, null=True)
    virtual_interface = models.ForeignKey(VirtualInterface, related_name='vlan_interface_set', db_column='virtualinterfaceid', blank=True, null=True)
    vlan = models.ForeignKey(Vlan, related_name='vlan_interface_set', db_column='vlanid', blank=True, null=True)
    ipv4enabled = models.IntegerField(blank=True, null=True)
    ipv4hostname = models.CharField(max_length=255, blank=True)
    ipv6enabled = models.IntegerField(blank=True, null=True)
    ipv6hostname = models.CharField(max_length=255, blank=True)
    mcastenabled = models.IntegerField(blank=True, null=True)
    irrdbfilter = models.IntegerField(blank=True, null=True)
    bgpmd5secret = models.CharField(max_length=255, blank=True)
    ipv4bgpmd5secret = models.CharField(max_length=255, blank=True)
    ipv6bgpmd5secret = models.CharField(max_length=255, blank=True)
    maxbgpprefix = models.IntegerField(blank=True, null=True)
    rsclient = models.IntegerField(blank=True, null=True)
    ipv4canping = models.IntegerField(blank=True, null=True)
    ipv6canping = models.IntegerField(blank=True, null=True)
    ipv4monitorrcbgp = models.IntegerField(blank=True, null=True)
    ipv6monitorrcbgp = models.IntegerField(blank=True, null=True)
    as112client = models.IntegerField(blank=True, null=True)
    busyhost = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'vlaninterface'

