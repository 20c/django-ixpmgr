from .settings import VERSIONED_APP

if VERSIONED_APP == "v5":
    from django_ixpmgr.v5.const import *
elif VERSIONED_APP == "v3":
    from django_ixpmgr.v3.const import *

# TODO - gen from perl?
# ../IXP-Manager/tools/perl-lib/IXPManager/lib/IXPManager/Const.pm
# gen from PHP better, but it's all spread out

# application/Entities/Customer.php
TYPE_FULL = 1
TYPE_ASSOCIATE = 2
TYPE_INTERNAL = 3
TYPE_IXP = 3
TYPE_PROBONO = 4

#    public static $CUST_TYPES_TEXT = [
#        self::TYPE_FULL      => 'Full',
#        self::TYPE_ASSOCIATE => 'Associate',
#        self::TYPE_INTERNAL  => 'Internal',
#        self::TYPE_PROBONO   => 'Pro-bono'

STATUS_NORMAL = 1
STATUS_NOTCONNECTED = 2
STATUS_SUSPENDED = 3

#    public static $CUST_STATUS_TEXT = [
#        self::STATUS_NORMAL           => 'Normal',
#        self::STATUS_NOTCONNECTED     => 'Not Connected',
#        self::STATUS_SUSPENDED        => 'Suspended',
#    ];


# application/Entities/PhysicalInterface.php

STATUS_CONNECTED = 1
STATUS_DISABLED = 2
STATUS_NOTCONNECTED = 3
STATUS_XCONNECT = 4
STATUS_QUARANTINE = 5

portstatus_desc = {
    (STATUS_CONNECTED, "Connected"),
    (STATUS_DISABLED, "Disabled"),
    (STATUS_NOTCONNECTED, "Not Connected"),
    (STATUS_XCONNECT, "Awaiting X-Connect"),
    (STATUS_QUARANTINE, "Quarantine"),
}


# application/Entities/Switcher.php
# switch types
SWITCHTYPE_SWITCH = 1
SWITCHTYPE_CONSOLESERVER = 2

switchtype_desc = {
    (SWITCHTYPE_SWITCH, "Switch"),
    (SWITCHTYPE_CONSOLESERVER, "Console Server"),
}
