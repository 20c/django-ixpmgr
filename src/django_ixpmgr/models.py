from .settings import VERSIONED_APP

# TODO: look into dynamic from X import *

if VERSIONED_APP == "v5":
    from django_ixpmgr.v5.models import *
elif VERSIONED_APP == "v3":
    from django_ixpmgr.v3.models import *
else:
    raise ValueError(
        f"Could not load models for version {VERSIONED_APP}"
    )
