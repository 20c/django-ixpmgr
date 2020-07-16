from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor


class ProxyManager(models.Manager):
    def create(self, **k):
        proxy_fields = getattr(self.model, 'proxy_fields', set())
        values = {
            key: k.pop(key)
            for key in proxy_fields if key in k
        }
        obj = super(ProxyManager, self).create(**k)
        for key, value in values.items():
            setattr(obj, key, value)
        return obj

class ProxyFieldMixin:
    def contribute_to_class(self, model, name, **_):
        sup = super(ProxyFieldMixin, self)
        contrib = getattr(sup, 'contribute_to_class', None)
        if contrib:
            contrib(model, name, virtual_only=True)
        setattr(model, name, self)
        model.proxy_fields = getattr(model, 'proxy_fields', set())
        model.proxy_fields.add(name)

    def __set__(self, instance, value):
        model = self.proxy_model
        if model and not isinstance(value, model):
            value = model(value)
        setattr(instance, self.source_field_name, value)
        print('proxy set', instance, self.source_field_name, value)

    def __get__(self, instance, instance_type=None):
        value = getattr(instance, self.source_field_name)
        model = self.proxy_model
        if model and not isinstance(value, model):
            return model.objects.get(pk=value.id)
        return value

def ProxyField(field, *args, proxy_model=None, **kwargs):
    field_name = None
    if isinstance(field, DeferredAttribute):
        field_name = field.field_name
    elif isinstance(field, ForwardOneToOneDescriptor):
        field_name = field.field.name
    ParentField = field.__class__
    CustomProxyField = type("CustomProxyField", (ProxyFieldMixin, ParentField), {})

    self = CustomProxyField(field_name, *args, **kwargs)
    self.source_field_name = field_name
    self.proxy_model = proxy_model
    # self.descriptor_class # django3
    self.is_relation = False
    return self
