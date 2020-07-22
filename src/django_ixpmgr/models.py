from packaging import version as _version


def detect_version():
    return "5.7"


# Wrap models module corresponding to IXP-Manager version
IXPMGR_VERSION = _version.parse(detect_version())


def _should_import(v):
    return IXPMGR_VERSION >= _version.parse(v)


if _should_import("5.7"):
    from .v57.models import *
elif _should_import("3.7"):
    from .v37.models import *
