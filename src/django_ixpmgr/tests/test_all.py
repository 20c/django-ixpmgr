from django_ixpmgr.settings import VERSIONED_APP

if VERSIONED_APP == "v3":
    from ._test_v3 import *
elif VERSIONED_APP == "v5":
    from ._test_v5 import *
else:
    raise ValueError("Invalid VERSIONED_APP in test config")
