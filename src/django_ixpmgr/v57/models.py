# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiKeys(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    apikey = models.CharField(db_column='apiKey', unique=True, max_length=255)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    allowedips = models.TextField(db_column='allowedIPs', blank=True, null=True)  # Field name made lowercase.
    created = models.DateTimeField()
    lastseenat = models.DateTimeField(db_column='lastseenAt', blank=True, null=True)  # Field name made lowercase.
    lastseenfrom = models.CharField(db_column='lastseenFrom', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'api_keys'


class BgpSessions(models.Model):
    srcipaddressid = models.IntegerField()
    protocol = models.IntegerField()
    dstipaddressid = models.IntegerField()
    packetcount = models.IntegerField()
    last_seen = models.DateTimeField()
    source = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bgp_sessions'
        unique_together = (('srcipaddressid', 'protocol', 'dstipaddressid'),)


class Bgpsessiondata(models.Model):
    srcipaddressid = models.IntegerField(blank=True, null=True)
    dstipaddressid = models.IntegerField(blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    vlan = models.IntegerField(blank=True, null=True)
    packetcount = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bgpsessiondata'


class Cabinet(models.Model):
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    cololocation = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    u_counts_from = models.SmallIntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cabinet'


class CompanyBillingDetail(models.Model):
    billingcontactname = models.CharField(db_column='billingContactName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingaddress1 = models.CharField(db_column='billingAddress1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingaddress2 = models.CharField(db_column='billingAddress2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingaddress3 = models.CharField(db_column='billingAddress3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingtowncity = models.CharField(db_column='billingTownCity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingpostcode = models.CharField(db_column='billingPostcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingcountry = models.CharField(db_column='billingCountry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingemail = models.CharField(db_column='billingEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingtelephone = models.CharField(db_column='billingTelephone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vatnumber = models.CharField(db_column='vatNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vatrate = models.CharField(db_column='vatRate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    purchaseorderrequired = models.IntegerField(db_column='purchaseOrderRequired')  # Field name made lowercase.
    invoicemethod = models.CharField(db_column='invoiceMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    invoiceemail = models.CharField(db_column='invoiceEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    billingfrequency = models.CharField(db_column='billingFrequency', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_billing_detail'


class CompanyRegistrationDetail(models.Model):
    registeredname = models.CharField(db_column='registeredName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    companynumber = models.CharField(db_column='companyNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jurisdiction = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    address3 = models.CharField(max_length=255, blank=True, null=True)
    towncity = models.CharField(db_column='townCity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    postcode = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_registration_detail'


class ConsoleServer(models.Model):
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    serialnumber = models.CharField(db_column='serialNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'console_server'


class Consoleserverconnection(models.Model):
    custid = models.ForeignKey('Cust', models.DO_NOTHING, db_column='custid', blank=True, null=True)
    console_server = models.ForeignKey(ConsoleServer, models.DO_NOTHING, blank=True, null=True)
    switchid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    parity = models.IntegerField(blank=True, null=True)
    stopbits = models.IntegerField(blank=True, null=True)
    flowcontrol = models.IntegerField(blank=True, null=True)
    autobaud = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consoleserverconnection'
        unique_together = (('console_server', 'port'),)


class Contact(models.Model):
    custid = models.ForeignKey('Cust', models.DO_NOTHING, db_column='custid', blank=True, null=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    facilityaccess = models.IntegerField()
    mayauthorize = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    lastupdated = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=32, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContactGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    contact = models.OneToOneField(Contact, models.DO_NOTHING, primary_key=True)
    contact_group = models.ForeignKey(ContactGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'contact_to_group'
        unique_together = (('contact', 'contact_group'),)


class Corebundles(models.Model):
    description = models.CharField(max_length=255)
    type = models.IntegerField()
    graph_title = models.CharField(max_length=255)
    bfd = models.IntegerField()
    ipv4_subnet = models.CharField(max_length=18, blank=True, null=True)
    ipv6_subnet = models.CharField(max_length=43, blank=True, null=True)
    stp = models.IntegerField()
    cost = models.PositiveIntegerField(blank=True, null=True)
    preference = models.PositiveIntegerField(blank=True, null=True)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'corebundles'


class Coreinterfaces(models.Model):
    physical_interface = models.OneToOneField('Physicalinterface', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coreinterfaces'


class Corelinks(models.Model):
    core_interface_sidea = models.OneToOneField(Coreinterfaces, models.DO_NOTHING)
    core_interface_sideb = models.OneToOneField(Coreinterfaces, models.DO_NOTHING)
    core_bundle = models.ForeignKey(Corebundles, models.DO_NOTHING)
    bfd = models.IntegerField()
    ipv4_subnet = models.CharField(max_length=18, blank=True, null=True)
    ipv6_subnet = models.CharField(max_length=43, blank=True, null=True)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'corelinks'


class Cust(models.Model):
    company_registered_detail = models.OneToOneField(CompanyRegistrationDetail, models.DO_NOTHING, blank=True, null=True)
    company_billing_details = models.OneToOneField(CompanyBillingDetail, models.DO_NOTHING, blank=True, null=True)
    irrdb = models.ForeignKey('Irrdbconfig', models.DO_NOTHING, db_column='irrdb', blank=True, null=True)
    reseller = models.ForeignKey('self', models.DO_NOTHING, db_column='reseller', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True, null=True)
    abbreviatedname = models.CharField(db_column='abbreviatedName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    autsys = models.IntegerField(blank=True, null=True)
    maxprefixes = models.IntegerField(blank=True, null=True)
    peeringemail = models.CharField(max_length=255, blank=True, null=True)
    nocphone = models.CharField(max_length=255, blank=True, null=True)
    noc24hphone = models.CharField(max_length=255, blank=True, null=True)
    nocfax = models.CharField(max_length=255, blank=True, null=True)
    nocemail = models.CharField(max_length=255, blank=True, null=True)
    nochours = models.CharField(max_length=255, blank=True, null=True)
    nocwww = models.CharField(max_length=255, blank=True, null=True)
    peeringmacro = models.CharField(max_length=255, blank=True, null=True)
    peeringmacrov6 = models.CharField(max_length=255, blank=True, null=True)
    peeringpolicy = models.CharField(max_length=255, blank=True, null=True)
    corpwww = models.CharField(max_length=255, blank=True, null=True)
    datejoin = models.DateField(blank=True, null=True)
    dateleave = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    activepeeringmatrix = models.IntegerField(blank=True, null=True)
    lastupdated = models.DateField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    md5support = models.CharField(db_column='MD5Support', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isreseller = models.IntegerField(db_column='isReseller')  # Field name made lowercase.
    in_manrs = models.IntegerField()
    in_peeringdb = models.IntegerField()
    peeringdb_oauth = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cust'


class CustNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Cust, models.DO_NOTHING)
    private = models.IntegerField()
    title = models.CharField(max_length=255)
    note = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cust_notes'


class CustTag(models.Model):
    tag = models.CharField(unique=True, max_length=255)
    display_as = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    internal_only = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cust_tag'


class CustToCustTag(models.Model):
    customer_tag = models.OneToOneField(CustTag, models.DO_NOTHING, primary_key=True)
    customer = models.ForeignKey(Cust, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cust_to_cust_tag'
        unique_together = (('customer_tag', 'customer'),)


class Custkit(models.Model):
    custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='custid', blank=True, null=True)
    cabinetid = models.ForeignKey(Cabinet, models.DO_NOTHING, db_column='cabinetid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custkit'


class CustomerToIxp(models.Model):
    customer = models.OneToOneField(Cust, models.DO_NOTHING, primary_key=True)
    ixp = models.ForeignKey('Ixp', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customer_to_ixp'
        unique_together = (('customer', 'ixp'),)


class CustomerToUsers(models.Model):
    customer = models.ForeignKey(Cust, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    privs = models.IntegerField()
    extra_attributes = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_login_date = models.DateTimeField(blank=True, null=True)
    last_login_from = models.TextField(blank=True, null=True)
    last_login_via = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_to_users'
        unique_together = (('customer', 'user'),)


class DocstoreCustomerDirectories(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Cust, models.DO_NOTHING)
    parent_dir_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docstore_customer_directories'


class DocstoreCustomerFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Cust, models.DO_NOTHING)
    docstore_customer_directory = models.ForeignKey(DocstoreCustomerDirectories, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    disk = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    sha256 = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    min_privs = models.SmallIntegerField()
    file_last_updated = models.DateTimeField()
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docstore_customer_files'


class DocstoreDirectories(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_dir_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docstore_directories'


class DocstoreFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    docstore_directory = models.ForeignKey(DocstoreDirectories, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    disk = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    sha256 = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    min_privs = models.SmallIntegerField()
    file_last_updated = models.DateTimeField()
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docstore_files'


class DocstoreLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    docstore_file = models.ForeignKey(DocstoreFiles, models.DO_NOTHING)
    downloaded_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docstore_logs'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Infrastructure(models.Model):
    ixp = models.ForeignKey('Ixp', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    shortname = models.CharField(max_length=255, blank=True, null=True)
    isprimary = models.IntegerField(db_column='isPrimary')  # Field name made lowercase.
    peeringdb_ix_id = models.BigIntegerField(blank=True, null=True)
    ixf_ix_id = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infrastructure'
        unique_together = (('shortname', 'ixp'),)


class Ipv4Address(models.Model):
    vlanid = models.ForeignKey('Vlan', models.DO_NOTHING, db_column='vlanid', blank=True, null=True)
    address = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipv4address'
        unique_together = (('vlanid', 'address'),)


class Ipv6Address(models.Model):
    vlanid = models.ForeignKey('Vlan', models.DO_NOTHING, db_column='vlanid', blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipv6address'
        unique_together = (('vlanid', 'address'),)


class IrrdbAsn(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Cust, models.DO_NOTHING)
    asn = models.IntegerField()
    protocol = models.IntegerField()
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'irrdb_asn'
        unique_together = (('asn', 'protocol', 'customer'),)


class IrrdbPrefix(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Cust, models.DO_NOTHING)
    prefix = models.CharField(max_length=255)
    protocol = models.IntegerField()
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'irrdb_prefix'
        unique_together = (('prefix', 'protocol', 'customer'),)


class Irrdbconfig(models.Model):
    host = models.CharField(max_length=255, blank=True, null=True)
    protocol = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'irrdbconfig'


class Ixp(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    address3 = models.CharField(max_length=255, blank=True, null=True)
    address4 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ixp'


class L2Address(models.Model):
    vlan_interface = models.ForeignKey('Vlaninterface', models.DO_NOTHING)
    mac = models.CharField(max_length=12, blank=True, null=True)
    firstseen = models.DateTimeField(blank=True, null=True)
    lastseen = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'l2address'
        unique_together = (('mac', 'vlan_interface'),)


class Location(models.Model):
    pdb_facility_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    shortname = models.CharField(unique=True, max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    nocphone = models.CharField(max_length=255, blank=True, null=True)
    nocfax = models.CharField(max_length=255, blank=True, null=True)
    nocemail = models.CharField(max_length=255, blank=True, null=True)
    officephone = models.CharField(max_length=255, blank=True, null=True)
    officefax = models.CharField(max_length=255, blank=True, null=True)
    officeemail = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Logos(models.Model):
    customer = models.ForeignKey(Cust, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    stored_name = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'logos'


class Macaddress(models.Model):
    virtualinterfaceid = models.ForeignKey('Virtualinterface', models.DO_NOTHING, db_column='virtualinterfaceid', blank=True, null=True)
    firstseen = models.DateTimeField(blank=True, null=True)
    lastseen = models.DateTimeField(blank=True, null=True)
    mac = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'macaddress'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Netinfo(models.Model):
    vlan = models.ForeignKey('Vlan', models.DO_NOTHING)
    protocol = models.IntegerField()
    property = models.CharField(max_length=255)
    ix = models.IntegerField()
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'netinfo'


class Networkinfo(models.Model):
    vlanid = models.ForeignKey('Vlan', models.DO_NOTHING, db_column='vlanid', blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    network = models.CharField(max_length=255, blank=True, null=True)
    masklen = models.IntegerField(blank=True, null=True)
    rs1address = models.CharField(max_length=40, blank=True, null=True)
    rs2address = models.CharField(max_length=40, blank=True, null=True)
    dnsfile = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'networkinfo'


class Oui(models.Model):
    oui = models.CharField(unique=True, max_length=6)
    organisation = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oui'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class PatchPanel(models.Model):
    cabinet = models.ForeignKey(Cabinet, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    colo_reference = models.CharField(max_length=255)
    cable_type = models.IntegerField()
    connector_type = models.IntegerField()
    installation_date = models.DateTimeField(blank=True, null=True)
    port_prefix = models.CharField(max_length=10)
    chargeable = models.IntegerField()
    location_notes = models.TextField()
    active = models.IntegerField()
    u_position = models.IntegerField(blank=True, null=True)
    mounted_at = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patch_panel'


class PatchPanelPort(models.Model):
    switch_port = models.OneToOneField('Switchport', models.DO_NOTHING, blank=True, null=True)
    patch_panel = models.ForeignKey(PatchPanel, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Cust, models.DO_NOTHING, blank=True, null=True)
    duplex_master = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    number = models.SmallIntegerField()
    state = models.IntegerField()
    colo_circuit_ref = models.CharField(max_length=255, blank=True, null=True)
    colo_billing_ref = models.CharField(max_length=255, blank=True, null=True)
    ticket_ref = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    private_notes = models.TextField(blank=True, null=True)
    assigned_at = models.DateField(blank=True, null=True)
    connected_at = models.DateField(blank=True, null=True)
    cease_requested_at = models.DateField(blank=True, null=True)
    ceased_at = models.DateField(blank=True, null=True)
    last_state_change = models.DateField(blank=True, null=True)
    internal_use = models.IntegerField()
    chargeable = models.IntegerField()
    owned_by = models.IntegerField()
    loa_code = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patch_panel_port'


class PatchPanelPortFile(models.Model):
    patch_panel_port = models.ForeignKey(PatchPanelPort, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    uploaded_by = models.CharField(max_length=255)
    size = models.IntegerField()
    is_private = models.IntegerField()
    storage_location = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'patch_panel_port_file'


class PatchPanelPortHistory(models.Model):
    patch_panel_port = models.ForeignKey(PatchPanelPort, models.DO_NOTHING, blank=True, null=True)
    duplex_master = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    number = models.SmallIntegerField()
    state = models.IntegerField()
    colo_circuit_ref = models.CharField(max_length=255, blank=True, null=True)
    colo_billing_ref = models.CharField(max_length=255, blank=True, null=True)
    ticket_ref = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    private_notes = models.TextField(blank=True, null=True)
    assigned_at = models.DateField(blank=True, null=True)
    connected_at = models.DateField(blank=True, null=True)
    cease_requested_at = models.DateField(blank=True, null=True)
    ceased_at = models.DateField(blank=True, null=True)
    internal_use = models.IntegerField()
    chargeable = models.IntegerField()
    owned_by = models.IntegerField()
    cust_id = models.IntegerField(blank=True, null=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    switchport = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patch_panel_port_history'


class PatchPanelPortHistoryFile(models.Model):
    patch_panel_port_history = models.ForeignKey(PatchPanelPortHistory, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    uploaded_by = models.CharField(max_length=255)
    size = models.IntegerField()
    is_private = models.IntegerField()
    storage_location = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'patch_panel_port_history_file'


class PeeringManager(models.Model):
    custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='custid', blank=True, null=True)
    peerid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='peerid', blank=True, null=True)
    email_last_sent = models.DateTimeField(blank=True, null=True)
    emails_sent = models.IntegerField(blank=True, null=True)
    peered = models.IntegerField(blank=True, null=True)
    rejected = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peering_manager'


class PeeringMatrix(models.Model):
    x_custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='x_custid', blank=True, null=True)
    y_custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='y_custid', blank=True, null=True)
    vlan = models.IntegerField(blank=True, null=True)
    x_as = models.IntegerField(blank=True, null=True)
    y_as = models.IntegerField(blank=True, null=True)
    peering_status = models.CharField(max_length=255, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peering_matrix'


class Physicalinterface(models.Model):
    switchportid = models.OneToOneField('Switchport', models.DO_NOTHING, db_column='switchportid', blank=True, null=True)
    fanout_physical_interface = models.OneToOneField('self', models.DO_NOTHING, blank=True, null=True)
    virtualinterfaceid = models.ForeignKey('Virtualinterface', models.DO_NOTHING, db_column='virtualinterfaceid', blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    duplex = models.CharField(max_length=16, blank=True, null=True)
    autoneg = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physicalinterface'


class Routers(models.Model):
    vlan = models.ForeignKey('Vlan', models.DO_NOTHING)
    handle = models.CharField(unique=True, max_length=255)
    protocol = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=255)
    router_id = models.CharField(max_length=255)
    peering_ip = models.CharField(max_length=255)
    asn = models.PositiveIntegerField()
    software = models.CharField(max_length=255)
    software_version = models.CharField(max_length=255, blank=True, null=True)
    operating_system = models.CharField(max_length=255, blank=True, null=True)
    operating_system_version = models.CharField(max_length=255, blank=True, null=True)
    mgmt_host = models.CharField(max_length=255)
    api = models.CharField(max_length=255, blank=True, null=True)
    api_type = models.PositiveSmallIntegerField()
    lg_access = models.PositiveSmallIntegerField(blank=True, null=True)
    quarantine = models.IntegerField()
    bgp_lc = models.IntegerField()
    rpki = models.IntegerField()
    rfc1997_passthru = models.IntegerField()
    template = models.CharField(max_length=255)
    skip_md5 = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routers'


class RsPrefixes(models.Model):
    custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='custid', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    prefix = models.CharField(max_length=64, blank=True, null=True)
    protocol = models.IntegerField(blank=True, null=True)
    irrdb = models.IntegerField(blank=True, null=True)
    rs_origin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rs_prefixes'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_id = models.BigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'


class SflowReceiver(models.Model):
    virtual_interface = models.ForeignKey('Virtualinterface', models.DO_NOTHING, blank=True, null=True)
    dst_ip = models.CharField(max_length=255)
    dst_port = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sflow_receiver'


class Switch(models.Model):
    infrastructure = models.ForeignKey(Infrastructure, models.DO_NOTHING, db_column='infrastructure', blank=True, null=True)
    cabinetid = models.ForeignKey(Cabinet, models.DO_NOTHING, db_column='cabinetid', blank=True, null=True)
    vendorid = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendorid', blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    asn = models.PositiveIntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    mgmt_mac_address = models.CharField(max_length=12, blank=True, null=True)
    loopback_ip = models.CharField(unique=True, max_length=39, blank=True, null=True)
    loopback_name = models.CharField(max_length=255, blank=True, null=True)
    ipv4addr = models.CharField(max_length=255, blank=True, null=True)
    ipv6addr = models.CharField(max_length=255, blank=True, null=True)
    snmppasswd = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    osdate = models.DateTimeField(db_column='osDate', blank=True, null=True)  # Field name made lowercase.
    osversion = models.CharField(db_column='osVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='serialNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mausupported = models.IntegerField(db_column='mauSupported', blank=True, null=True)  # Field name made lowercase.
    lastpolled = models.DateTimeField(db_column='lastPolled', blank=True, null=True)  # Field name made lowercase.
    snmp_engine_time = models.BigIntegerField(blank=True, null=True)
    snmp_system_uptime = models.BigIntegerField(blank=True, null=True)
    snmp_engine_boots = models.BigIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'switch'


class Switchport(models.Model):
    switchid = models.ForeignKey(Switch, models.DO_NOTHING, db_column='switchid', blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    ifindex = models.IntegerField(db_column='ifIndex', blank=True, null=True)  # Field name made lowercase.
    ifname = models.CharField(db_column='ifName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ifalias = models.CharField(db_column='ifAlias', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ifhighspeed = models.IntegerField(db_column='ifHighSpeed', blank=True, null=True)  # Field name made lowercase.
    ifmtu = models.IntegerField(db_column='ifMtu', blank=True, null=True)  # Field name made lowercase.
    ifphysaddress = models.CharField(db_column='ifPhysAddress', max_length=17, blank=True, null=True)  # Field name made lowercase.
    ifadminstatus = models.IntegerField(db_column='ifAdminStatus', blank=True, null=True)  # Field name made lowercase.
    ifoperstatus = models.IntegerField(db_column='ifOperStatus', blank=True, null=True)  # Field name made lowercase.
    iflastchange = models.IntegerField(db_column='ifLastChange', blank=True, null=True)  # Field name made lowercase.
    lastsnmppoll = models.DateTimeField(db_column='lastSnmpPoll', blank=True, null=True)  # Field name made lowercase.
    lagifindex = models.IntegerField(db_column='lagIfIndex', blank=True, null=True)  # Field name made lowercase.
    mautype = models.CharField(db_column='mauType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    maustate = models.CharField(db_column='mauState', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mauavailability = models.CharField(db_column='mauAvailability', max_length=255, blank=True, null=True)  # Field name made lowercase.
    maujacktype = models.CharField(db_column='mauJacktype', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mauautonegsupported = models.IntegerField(db_column='mauAutoNegSupported', blank=True, null=True)  # Field name made lowercase.
    mauautonegadminstate = models.IntegerField(db_column='mauAutoNegAdminState', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'switchport'


class TelescopeEntries(models.Model):
    sequence = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    batch_id = models.CharField(max_length=36)
    family_hash = models.CharField(max_length=255, blank=True, null=True)
    should_display_on_index = models.IntegerField()
    type = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telescope_entries'


class TelescopeEntriesTags(models.Model):
    entry_uuid = models.ForeignKey(TelescopeEntries, models.DO_NOTHING, db_column='entry_uuid')
    tag = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'telescope_entries_tags'


class TelescopeMonitoring(models.Model):
    tag = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'telescope_monitoring'


class Traffic95Th(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Cust, models.DO_NOTHING, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    average = models.BigIntegerField(blank=True, null=True)
    max = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_95th'


class Traffic95ThMonthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Cust, models.DO_NOTHING, blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    max_95th = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_95th_monthly'


class TrafficDaily(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Cust, models.DO_NOTHING)
    ixp = models.ForeignKey(Ixp, models.DO_NOTHING)
    day = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)
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


class TrafficDailyPhysInts(models.Model):
    id = models.BigAutoField(primary_key=True)
    physicalinterface = models.ForeignKey(Physicalinterface, models.DO_NOTHING)
    day = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)
    day_avg_in = models.BigIntegerField(blank=True, null=True)
    day_avg_out = models.BigIntegerField(blank=True, null=True)
    day_max_in = models.BigIntegerField(blank=True, null=True)
    day_max_out = models.BigIntegerField(blank=True, null=True)
    day_max_in_at = models.DateTimeField(blank=True, null=True)
    day_max_out_at = models.DateTimeField(blank=True, null=True)
    day_tot_in = models.BigIntegerField(blank=True, null=True)
    day_tot_out = models.BigIntegerField(blank=True, null=True)
    week_avg_in = models.BigIntegerField(blank=True, null=True)
    week_avg_out = models.BigIntegerField(blank=True, null=True)
    week_max_in = models.BigIntegerField(blank=True, null=True)
    week_max_out = models.BigIntegerField(blank=True, null=True)
    week_max_in_at = models.DateTimeField(blank=True, null=True)
    week_max_out_at = models.DateTimeField(blank=True, null=True)
    week_tot_in = models.BigIntegerField(blank=True, null=True)
    week_tot_out = models.BigIntegerField(blank=True, null=True)
    month_avg_in = models.BigIntegerField(blank=True, null=True)
    month_avg_out = models.BigIntegerField(blank=True, null=True)
    month_max_in = models.BigIntegerField(blank=True, null=True)
    month_max_out = models.BigIntegerField(blank=True, null=True)
    month_max_in_at = models.DateTimeField(blank=True, null=True)
    month_max_out_at = models.DateTimeField(blank=True, null=True)
    month_tot_in = models.BigIntegerField(blank=True, null=True)
    month_tot_out = models.BigIntegerField(blank=True, null=True)
    year_avg_in = models.BigIntegerField(blank=True, null=True)
    year_avg_out = models.BigIntegerField(blank=True, null=True)
    year_max_in = models.BigIntegerField(blank=True, null=True)
    year_max_out = models.BigIntegerField(blank=True, null=True)
    year_max_in_at = models.DateTimeField(blank=True, null=True)
    year_max_out_at = models.DateTimeField(blank=True, null=True)
    year_tot_in = models.BigIntegerField(blank=True, null=True)
    year_tot_out = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traffic_daily_phys_ints'


class User(models.Model):
    custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='custid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    authorisedmobile = models.CharField(db_column='authorisedMobile', max_length=30, blank=True, null=True)  # Field name made lowercase.
    uid = models.IntegerField(blank=True, null=True)
    privs = models.IntegerField(blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)
    peeringdb_id = models.BigIntegerField(unique=True, blank=True, null=True)
    extra_attributes = models.TextField(blank=True, null=True)  # This field type is a guess.
    lastupdated = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class User2Fa(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING)
    enabled = models.IntegerField()
    secret = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_2fa'


class UserLogins(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_to_user = models.ForeignKey(CustomerToUsers, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=39)
    at = models.DateTimeField()
    via = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_logins'


class UserPref(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    ix = models.IntegerField()
    op = models.CharField(max_length=2, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    expire = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'user_pref'
        unique_together = (('user', 'attribute', 'op', 'ix'),)


class UserRememberTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    token = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    ip = models.CharField(max_length=39)
    created = models.DateTimeField()
    expires = models.DateTimeField()
    is_2fa_complete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_remember_tokens'
        unique_together = (('user', 'token'),)


class Vendor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    shortname = models.CharField(max_length=255, blank=True, null=True)
    nagios_name = models.CharField(max_length=255, blank=True, null=True)
    bundle_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor'


class Virtualinterface(models.Model):
    custid = models.ForeignKey(Cust, models.DO_NOTHING, db_column='custid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    mtu = models.IntegerField(blank=True, null=True)
    trunk = models.IntegerField(blank=True, null=True)
    channelgroup = models.IntegerField(blank=True, null=True)
    lag_framing = models.IntegerField()
    fastlacp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'virtualinterface'


class Vlan(models.Model):
    infrastructureid = models.ForeignKey(Infrastructure, models.DO_NOTHING, db_column='infrastructureid')
    name = models.CharField(max_length=255, blank=True, null=True)
    config_name = models.CharField(max_length=32, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    private = models.IntegerField()
    peering_matrix = models.IntegerField()
    peering_manager = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vlan'
        unique_together = (('infrastructureid', 'config_name'),)


class Vlaninterface(models.Model):
    ipv4addressid = models.OneToOneField(Ipv4Address, models.DO_NOTHING, db_column='ipv4addressid', blank=True, null=True)
    ipv6addressid = models.OneToOneField(Ipv6Address, models.DO_NOTHING, db_column='ipv6addressid', blank=True, null=True)
    virtualinterfaceid = models.ForeignKey(Virtualinterface, models.DO_NOTHING, db_column='virtualinterfaceid', blank=True, null=True)
    vlanid = models.ForeignKey(Vlan, models.DO_NOTHING, db_column='vlanid', blank=True, null=True)
    ipv4enabled = models.IntegerField(blank=True, null=True)
    ipv4hostname = models.CharField(max_length=255, blank=True, null=True)
    ipv6enabled = models.IntegerField(blank=True, null=True)
    ipv6hostname = models.CharField(max_length=255, blank=True, null=True)
    mcastenabled = models.IntegerField(blank=True, null=True)
    irrdbfilter = models.IntegerField(blank=True, null=True)
    bgpmd5secret = models.CharField(max_length=255, blank=True, null=True)
    ipv4bgpmd5secret = models.CharField(max_length=255, blank=True, null=True)
    ipv6bgpmd5secret = models.CharField(max_length=255, blank=True, null=True)
    maxbgpprefix = models.IntegerField(blank=True, null=True)
    rsclient = models.IntegerField(blank=True, null=True)
    rsmorespecifics = models.IntegerField()
    ipv4canping = models.IntegerField(blank=True, null=True)
    ipv6canping = models.IntegerField(blank=True, null=True)
    ipv4monitorrcbgp = models.IntegerField(blank=True, null=True)
    ipv6monitorrcbgp = models.IntegerField(blank=True, null=True)
    as112client = models.IntegerField(blank=True, null=True)
    busyhost = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vlaninterface'
