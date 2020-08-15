"""
Utilities for defining proxy fields on proxy models which forward reads and
writes to a source field, and supporting functions.
"""
from typing import Union
from collections import namedtuple
from itertools import chain
from functools import wraps

from django.db import models
from django.db.models import sql
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor


# # convenient field stubbing
# def ConstField(value):
#     return property(lambda self: value)
# def NullField():
#     return ConstField(None)

class _ConstFieldDescriptor:
    def __init__(self, value):
        self.value = value

    def contribute_to_class(self, model, name, **_):
        model.proxies.add_proxy_field(name, None)

    def __get__(self, instance, instance_type=None):
        if instance is None: return self
        return None

    def __set__(self, instance, value):
        # print("warning: setting null field")
        pass


class ProxyManager(models.Manager):
    """Custom manager with factory method using named args corresponding to IX-API"""

    def __init__(self):
        super().__init__()
        # self.proxy_fields = set()
        self.proxy_fields = {}

    def add_proxy_field(self, name, source_name):
        """Register a field name as a proxy field. Regenerates the create() class method
        """
        # self.proxy_fields.add(name)
        self.proxy_fields[name] = source_name
        self.create = self.get_factory()

    def get_factory(self):
        """Generate a factory function with named args and docstring corresponding to
        registered proxy fields.

        >>> class MyMod(ProxyBase, BaseMod):
        >>>   class Meta: proxy = True
        >>>   name = ProxyField(BaseMod.nombre)
        >>> create = MyMod.proxies.get_factory()
        >>> create(name="Foo")
        <MyMod: MyMod object (1)>
        """
        args = self.writable_fields()
        arg_spec = ", ".join(f"{name}=None" for name in args)
        arg_list = ", ".join(f"{name}={name}" for name in args)
        doc_str = (
            f"Create, save, and return a new object; extends Django's `Manager.create`."
        )
        exec_lines = [
            f"def create({arg_spec}, **kwargs):",
            f"    \"{doc_str}\"",
            f"    return _create({arg_list}, **kwargs)",
        ]
        namespace = {"_create": self._create}
        exec("\n".join(exec_lines), namespace)
        return namespace["create"]

    def property(self, source):
        "Define a property and register a method as a proxy field"
        def decorator(func):
            self.add_proxy_field(func.__name__, get_field_name(source))
            return property(func)
        return decorator

    # FIXME: dev only
    def const_field(self, value):
        return _ConstFieldDescriptor(value)
    def null_field(self):
        return _ConstFieldDescriptor(None)

    def writable_fields(self):
        fields = self.proxy_fields.copy()
        fields.pop("pk", None)        # todo
        return fields

    def _create(self, **kwargs):
        # Intercept the proxy fields bc Django will choke on them
        values = {
            key: kwargs.pop(key)
            for key in self.writable_fields() if key in kwargs
        }
        # obj = super().create(**kwargs)
        obj = self.model(**kwargs)
        for key, value in values.items():
            # breakpoint()
            setattr(obj, key, value)
        obj.save()
        return obj


# Adapted from https://shezadkhan.com/aliasing-fields-in-django/
# Defines descriptors and a contribute_to_class method to plug into a Django
# model which uses ProxyManager.
# NB: the contribute_to_class is widely used but not a stable API; Django 3
# seems to be using a new `descriptor_class` attribute to do this.
# https://www.b-list.org/weblog/2019/mar/04/class/
# https://docs.python.org/3/reference/datamodel.html#descriptors
class _ProxyFieldMixin:
    """
    Mixin class for defining a proxy field.
    """
    def _init(self, field_name, relation, proxy_model): # todo: cleaner mixin ctor?
        self.field_name = field_name
        self.relation = relation
        self.proxy_model = proxy_model

    def contribute_to_class(self, model, name, **_):
        """Add this field to a model.
        Model must define a `.proxies` ProxyManager class attribute
        """
        contrib = getattr(super(), "contribute_to_class", None)
        if contrib:
            contrib(model, name)
        setattr(model, name, self)
        mgr = self.get_manager(model)
        mgr.add_proxy_field(name, self.field_name)
        # if mgr: mgr.add_proxy_field(name)

    def get_instance(self, instance):
        if self.source_relation:
            return getattr(instance, self.source_relation.name)
        return instance

    def get_manager(self, model):
        return model.proxies


class _DirectFieldDescriptor(_ProxyFieldMixin):
    def __set__(self, instance, value):
        """Set the source field to a value. If field is a relation to another
        proxied model, the value is wrapped with the proxy model before being set.
        """
        model = self.proxy_model
        if model and not isinstance(value, model):
            if value is not None:
                value = model(value)
        setattr(self.get_instance(instance), self.source_field_name, value)

    def __get__(self, instance, instance_type=None):
        """Get the source field's value. If field is a relation to another
        proxied model, the return value is wrapped with the proxy model.
        """
        if instance is None:
            return self
        value = getattr(self.get_instance(instance), self.source_field_name)
        if not value:
            return value
        model = self.proxy_model
        if model and not isinstance(value, model):
            return model.objects.get(pk=value.id)
        return value

def get_field_name(source):
    "Determine source field name"
    if isinstance(source, DeferredAttribute):
        return source.field_name  # django2 inconsistency
    elif isinstance(source, ForwardOneToOneDescriptor):
        return source.field.name

def ProxyField(source, *args, relation=None, proxy_model=None, **kwargs):
    """Returns an instance of a new subclass of the source field.
    Pass a field as `relation`, to obtain the source instance via the field attribute.
    Pass a model as `proxy_model` to treat the field as a relation to another proxied model.
    """
    field_name = get_field_name(source)
    ParentField = source.__class__
    CustomProxyField = type("CustomProxyField", (_DirectFieldDescriptor, ParentField), {})

    proxy = CustomProxyField(field_name, *args, **kwargs)
    proxy.source_field_name = field_name
    proxy.source_relation = relation
    proxy.proxy_model = proxy_model
    # .descriptor_class # django3
    # super(proxy, _DirectFieldDescriptor).__init__(field_name, relation, proxy_model)
    # _DirectFieldDescriptor._init(proxy, field_name, relation, proxy_model)
    proxy._init(field_name, relation, proxy_model)
    return proxy


def redirected_manager(to_model):
    """
    returns a manager instance that is re-directed at a
    different table.

    this is currently for edge cases and requires similar
    table schemas to work.

    currently only used on ipam.IpAddress to fetch from the
    correct table for each ip version

    Argument(s):

    - to_model (`Model`) - model class to redirect to on
    the db level
    """

    class RedirectedQuery(sql.Query):
        """
        sql query class that overrides which model meta
        to use to build the query.

        this is where target table (db_table) gets locked in
        """
        def get_meta(self):
            return to_model._meta

    class RedirectedQuerySet(models.QuerySet):
        """
        Django queryset that uses RedirectedQuery for its
        queries
        """
        def __init__(self, model=None, query=None, using=None, hints=None):
            super().__init__(model=model, query=query, using=using, hints=hints)
            self.query = query or RedirectedQuery(self.model)

    class RedirectedManager(models.Manager):
        """
        Django object manager that returns queryset redirected
        to the table associated with the model specified
        in `to_model`
        """
        def get_queryset(self):
            return RedirectedQuerySet(self.model, using=self._db)

    return RedirectedManager()


class MultiQuerySet(models.QuerySet):
    """
    Queryset that forwards to multiple querysets and combines the results
    """
    def __init__(self, querysets=None, model=None, query=None, using=None, hints=None):
        if model and querysets:
            raise ValueError("pass exactly one of model or querysets")
        if model:
            super().__init__(model=model, query=query, using=using, hints=hints)
        else:
            super().__init__()
            self.source_querysets = querysets or ()

    def filter(self, *args, **kwargs):
        return chain_querysets(
            qs.filter(*args, **kwargs) for qs in self.source_querysets
        )

    def all(self):
        return chain_querysets(self.source_querysets)

    def iterator(self):
        for qs in self.source_querysets:
            yield from qs


class MultiManager(models.Manager):
    """
    Object manager that forwards to multiple querysets and combines the results
    """
    def __init__(self, querysets):
        super().__init__()
        self.source_querysets = querysets

    def get_queryset(self):
        ret = MultiQuerySet()
        ret.source_querysets = self.source_querysets
        return ret


# can be made lazier
def chain_querysets(querysets):
    return list(chain(*querysets))
