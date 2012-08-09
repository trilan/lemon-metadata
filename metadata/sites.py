from django.db.models.base import ModelBase
from lemon import extradmin

from .admin import MetadataInline
from .options import ModelMetadata


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class NotRegisteredInAdmin(Exception):
    pass


class MetadataSite(object):

    inline_admin_class = MetadataInline

    def __init__(self):
        self._registry = {}

    def _append_inline_instance(self, model):
        model_admin = extradmin.site._registry.get(model)
        if not model_admin:
            raise NotRegisteredInAdmin(
                u'The model %s is not registered in admin' % model.__name__)

        inline_instance = self.inline_admin_class(model, extradmin.site)
        original_get_inline_instances = model_admin.get_inline_instances

        def get_inline_instances(request):
            inline_instances = original_get_inline_instances(request)
            return inline_instances + [inline_instance]

        model_admin.get_inline_instances = get_inline_instances

    def register(self, model_or_iterable, model_metadata_class=None, **options):
        if not model_metadata_class:
            model_metadata_class = ModelMetadata

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered(
                    u'The model %s already registered' % model.__name__)

            self._append_inline_instance(model)
            self._registry[model] = model_metadata_class(model, **options)


site = MetadataSite()
