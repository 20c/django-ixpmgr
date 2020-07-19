from collections import namedtuple

from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor

class ProxyManager(models.Manager):
    def __init__(self):
        super(ProxyManager, self).__init__()
        self.proxy_fields = set()

    def add_proxy_field(self, name):
        self.proxy_fields.add(name)
        self.create = self.get_factory()

    def get_factory(self):
        namespace = {'_create': self._create}
        args = self.proxy_fields
        arg_spec = ', '.join(f'{name}=None' for name in args)
        arg_list = ', '.join(f'{name}={name}' for name in args)
        exec(f'''def create({arg_spec}, **kwargs): return _create({arg_list}, **kwargs)''', namespace)
        return namespace['create']

    def _create(self, **k):
        values = {
            key: k.pop(key)
            for key in self.proxy_fields if key in k
        }
        obj = super(ProxyManager, self).create(**k)
        for key, value in values.items():
            setattr(obj, key, value)
        obj.save()
        return obj


class ProxyModel(models.Model):
    class Meta:
        abstract = True
        # proxy = True
    proxies = ProxyManager()


class ProxyFieldMixin:
    def contribute_to_class(self, model, name, **_):
        sup = super(ProxyFieldMixin, self)
        contrib = getattr(sup, 'contribute_to_class', None)
        if contrib:
            contrib(model, name, virtual_only=True)
        setattr(model, name, self)
        model.proxies.add_proxy_field(name)

    def __set__(self, instance, value):
        model = self.proxy_model
        if model and not isinstance(value, model):
            value = model(value)
        setattr(instance, self.source_field_name, value)

    def __get__(self, instance, instance_type=None):
        value = getattr(instance, self.source_field_name)
        if not value: return value
        model = self.proxy_model
        if model and not isinstance(value, model):
            return model.objects.get(pk=value.id)
        return value


def ProxyField(field, *args, proxy_model=None, **kwargs):
    field_name = None
    if isinstance(field, DeferredAttribute):
        field_name = field.field_name # django2 inconsistency
    elif isinstance(field, ForwardOneToOneDescriptor):
        field_name = field.field.name
    ParentField = field.__class__
    _ProxyField = type("ProxyField", (ProxyFieldMixin, ParentField), {})

    self = _ProxyField(field_name, *args, **kwargs)
    # self.source_field = field
    self.source_field_name = field_name
    self.proxy_model = proxy_model
    # self.descriptor_class # django3
    # self.is_relation = False
    return self


def NullField():
    return property(lambda self: None)
