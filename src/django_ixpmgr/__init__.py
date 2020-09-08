from .settings import VERSIONED_APP

if VERSIONED_APP == "v5":
    from django_ixpmgr.v5 import IxpManagerAppConfig
elif VERSIONED_APP == "v3":
    from django_ixpmgr.v3 import IxpManagerAppConfig
