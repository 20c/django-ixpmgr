# Defining a new endpoint #

Taking a top-down approach, start by adding definitions for urls and views.
Django makes most of this very straightforward. Using `/accounts/` as an example:

```py
# views.py
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

# urls.py
router = rest_framework.routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet)
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

Once the mapped IXP-Manager table is identified, define the new object.

Note: these are currently defined in `{name}/models.py` for each of the five IX-API namespaces and moving them breaks the integration with `ixapi_schema` - their API serializers have hardcoded references to models by name, e.g. `"crm.Account"`, so in order for Django to find our models, this needs to live in `crm/models.py` for now.

```py
import django_ixpmgr.v57.models as ixpmgr_models
from django_ixpmgr.model_util import ProxyField, ProxyManager

class RegAddress(ixpmgr_models.CompanyRegistrationDetail):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.CompanyRegistrationDetail

    locality = ProxyField(Source.towncity)
    @property
    def street_address(self): return ...

class Account(ixpmgr_models.Cust):
    class Meta: proxy = True
    proxies = ProxyManager()
    Source = ixpmgr_models.Cust

    name = ProxyField(Source.shortname) # for demo
    address = ProxyField(Source.company_registered_detail, proxy_model=RegAddress)
```

DRF is mostly indifferent about how the serialized fields work, so we can use a mix of property methods, proxy fields , and simply inheriting fields from the backend model.

`ProxyManager` is just used for convenient testing now but it may be useful in the future for certain queries or doing writes. The `ProxyField`s register themselves in this manager.

## Polymorphic entities ##

This process is somewhat more involved with polymorphic models, but with a couple utility classes it's still pretty concise.

Write a serializer for the concrete model as normal; then extend the `PolymorphicSerializer` class and add a mapping to the implementation serializers:

```py
class ExchangeLanNetworkServiceSerializer(
    ixser.ExchangeLanNetworkService,
    serializers.ModelSerializer):
    class Meta:
        model = ExchangeLanNetworkService
    ...

class NetworkServiceSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        ExchangeLanNetworkService: ExchangeLanNetworkServiceSerializer, ...
    }
```

Define a view set that extends the `PolymorphicViewSet` and add the polymorphic serializer to it. `get_queryset` will gather the "child" classes mapped in the serializer and dispatch to them.

Because the queryset is defined like this, we also need to specify a basename for the router when registering the view (https://www.django-rest-framework.org/api-guide/routers/#Usage):

```py
class NetworkServiceViewSet(PolymorphicViewSet):
    serializer_class = serializers.NetworkServiceSerializer

router.register(r"member-joining-rules", views.MemberJoiningRuleViewSet, basename='member-joining-rules')
```
