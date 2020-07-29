"""
Utilities for defining proxy fields on proxy models which forward reads and
writes to a source field, and supporting functions.
"""
from collections import namedtuple

from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor


class ProxyManager(models.Manager):
    """Custom manager with factory method using named args corresponding to IX-API"""

    def __init__(self):
        super().__init__()
        self.proxy_fields = set()

    def add_proxy_field(self, name):
        "Register a field name as a proxy field. Regenerates the create() class method"
        self.proxy_fields.add(name)
        self.create = self.get_factory()

    def get_factory(self):
        """Generate a factory function with named args corresponding to IX-API.

        >>> class MyMod(ProxyModel, BaseMod):
        >>>   proxies = ProxyManager()
        >>>   name = ProxyField(BaseMod.nombre)
        >>> create = MyMod.proxies.get_factory()
        >>> create(name="Foo")
        <MyMod: MyMod object (1)>
        """
        args = self.proxy_fields
        arg_spec = ", ".join(f"{name}=None" for name in args)
        arg_list = ", ".join(f"{name}={name}" for name in args)
        doc_str = (
            f"Create, save, and return a new object; extends Django's `Manager.create`."
        )
        exec_lines = [
            f"def create({arg_spec}, **kwargs):",
            f'    "{doc_str}"',
            f"    return _create({arg_list}, **kwargs)",
        ]
        namespace = {"_create": self._create}
        exec("\n".join(exec_lines), namespace)
        return namespace["create"]

    def _create(self, **k):
        # Intercept the proxy fields bc Django will choke on them
        values = {key: k.pop(key) for key in self.proxy_fields if key in k}
        obj = super().create(**k)
        for key, value in values.items():
            setattr(obj, key, value)
        obj.save()
        return obj


class ProxyModel(models.Model):
    "Abstract base class for proxy models. Defines a `.proxies` manager."

    class Meta:
        abstract = True
        # proxy = True

    proxies = ProxyManager()


# Adapted from https://shezadkhan.com/aliasing-fields-in-django/
# Defines descriptors and a contribute_to_class method to plug into a Django
# model which uses ProxyManager.
# NB: the contribute_to_class is widely used but not a stable API; Django 3
# seems to be using a new `descriptor_class` attribute to do this.
# https://www.b-list.org/weblog/2019/mar/04/class/
# https://docs.python.org/3/reference/datamodel.html#descriptors
class ProxyFieldMixin:
    """
    Mixin class for defining a proxy field.
    """

    def contribute_to_class(self, model, name, **_):
        """Add this field to a model.
        Model must define a `.proxies` ProxyManager class attribute
        """
        sup = super()
        contrib = getattr(sup, "contribute_to_class", None)
        if contrib:
            contrib(model, name)
        setattr(model, name, self)
        model.proxies.add_proxy_field(name)

    def __set__(self, instance, value):
        """Set the source field to a value. If field is a relation to another
        proxied model, the value is wrapped with the proxy model before being set.
        """
        model = self.proxy_model
        if model and not isinstance(value, model):
            if value is not None:
                value = model(value)
        setattr(instance, self.source_field_name, value)

    def __get__(self, instance, instance_type=None):
        """Get the source field's value. If field is a relation to another
        proxied model, the return value is wrapped with the proxy model.
        """
        value = getattr(instance, self.source_field_name)
        if not value:
            return value
        model = self.proxy_model
        if model and not isinstance(value, model):
            return model.objects.get(pk=value.id)
        return value


def ProxyField(field, *args, proxy_model=None, **kwargs):
    """Returns an instance of a new subclass of the source field.
    If `proxy_model` is passed, the field is treated as a relation to another
    proxied model.
    """
    field_name = None
    if isinstance(field, DeferredAttribute):
        field_name = field.field_name  # django2 inconsistency
    elif isinstance(field, ForwardOneToOneDescriptor):
        field_name = field.field.name
    ParentField = field.__class__
    CustomProxyField = type("CustomProxyField", (ProxyFieldMixin, ParentField), {})

    self = CustomProxyField(field_name, *args, **kwargs)
    # self.source_field = field
    self.source_field_name = field_name
    self.proxy_model = proxy_model
    # self.descriptor_class # django3
    # self.is_relation = False
    return self


# convenient field stubbing
def NullField():
    return property(lambda self: None)
