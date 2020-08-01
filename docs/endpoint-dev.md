# Defining a new endpoint #

Taking a top-down approach, start by adding definitions for urls and views.
Django makes most of this very straightforward. Using `/accounts/` as an example:

```py
# urls.py
router = rest_framework.routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet)

# views.py
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
```

DRF serializers are next. The `ModelSerializer` works fine for basic proxies:

```py
import ixapi_schema.v2.schema as ixser

class AccountSerializer(ixser.Account, serializers.ModelSerializer):
    class Meta:
        many = True
        model = models.Account
        fields = [ "name", "address", ... ]
```

Once the endpoint and mapped IXP-Manager table are identified, define the new object.

Note: these are currently defined in `{name}/models.py` for each of the five IX-API namespaces and moving them breaks the integration with `ixapi_schema` - their API serializers have hardcoded references to models by name, e.g. `"crm.Account"`, so in order for Django to find our models, this needs to live in `crm/models.py` for now.

```py
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyField, ProxyManager

class Account(ixpmgr_models.Cust):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.Cust

    name = ProxyField(Source.shortname) # for demo
    address = ProxyField(Source.company_registered_detail, proxy_model=RegAddress)

class RegAddress(ixpmgr_models.CompanyRegistrationDetail):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.CompanyRegistrationDetail

    locality = ProxyField(Source.towncity)
    @property
    def street_address(self): return ...
```

DRF is mostly indifferent about how the serialized fields work, so we can use a mix of property methods, proxy fields , and simply inheriting fields from the backend model.

`ProxyManager` is just used for convenient testing now but it may be useful in the future for certain queries or doing writes. The `ProxyField`s register themselves in this manager.

## Polymorphic entities ##

This process is somewhat more involved with polymorphic models, but with a couple utility classes it's still pretty concise.

(to do)
