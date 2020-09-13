import semver
from django.conf import settings

# load config or defaults
HOME = getattr(settings, "IXPMGR_HOME", "/usr/local/ixp")

RDNS_DOMAIN = getattr(settings, "IXPMGR_RDNS_DOMAIN", "")
RDNS_FORMAT = getattr(
    settings,
    "IXPMGR_RDNS_FORMAT",
    "as{cust.autsys}.{intf}.{phy_intf.switchport.switch.name}",
)
RDNS_INTF_REGEX = getattr(settings, "IXPMGR_RDNS_INTF_REGEX", [("[ /]", "-")])
RDNS_IPV6_PREFIX_LEN = getattr(settings, "IXPMGR_RDNS_IPV6_PREFIX_LEN", 64)
RDNS_KEYRING = getattr(settings, "IXPMGR_RDNS_KEYRING", {})
RDNS_SERVER = getattr(settings, "IXPMGR_RDNS_SERVER", None)
RDNS_TTL = getattr(settings, "IXPMGR_RDNS_TTL", 86400)

# Ixp Manager version, needs to be set to a valid semantic version
# e.g., {major}.{minor}.{patch}
# Not providing default to require explicit setting
VERSION = getattr(settings, "IXPMGR_VERSION")

# Parse into semantic version info
SEMANTIC_VERSION = semver.VersionInfo.parse(VERSION)

# Determine versioned app to use according to parsed version
if SEMANTIC_VERSION.major == 5:
    VERSIONED_APP = "v5"
elif SEMANTIC_VERSION.major == 3:
    VERSIONED_APP = "v3"
else:
    raise ValueError(f"Unsupported ixp manager version: {VERSION}")
