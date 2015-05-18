
from django.conf import settings

# load config or defaults
HOME = getattr(settings, 'IXPMGR_HOME', '/usr/local/ixp')

RDNS_DOMAIN= getattr(settings, 'IXPMGR_RDNS_DOMAIN', '')
RDNS_FORMAT = getattr(settings, 'IXPMGR_RDNS_FORMAT', 'as{cust.autsys}.{intf}.{phy_intf.switchport.switch.name}')
RDNS_INTF_REGEX = getattr(settings, 'IXPMGR_RDNS_INTF_REGEX', [('[ /]', '-')])
RDNS_IPV6_PREFIX_LEN= getattr(settings, 'IXPMGR_RDNS_IPV6_PREFIX_LEN', 64)
RDNS_KEYRING = getattr(settings, 'IXPMGR_RDNS_KEYRING', {})
RDNS_SERVER = getattr(settings, 'IXPMGR_RDNS_SERVER', None)
RDNS_TTL= getattr(settings, 'IXPMGR_RDNS_TTL', 86400)



