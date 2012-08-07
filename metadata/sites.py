from django.db.models import ManyToManyField
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, pre_delete, m2m_changed

from lemon import extradmin

from .admin import MetadataInline
from .models import Metadata
from .options import ModelMetadata


class AlreadyRegistered(Exception):

    pass


class NotRegistered(Exception):

    pass


class MetadataSite(object):

    inline_admin_class = MetadataInline

    def __init__(self):
        self._registry = {}

    def _append_inline_instance(self, model):
        model_admin = extradmin.site._registry.get(model)
        if not model_admin:
            return

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

            if options:
                options['__module__'] = __name__
                model_metadata_class = type(
                    '%sMetadata' % model.__name__,
                    (model_metadata_class,), options)
            model_metadata = model_metadata_class()
            self._registry[model] = model_metadata

            pre_delete.connect(self.delete_metadata, sender=model)
            post_save.connect(self.check_metadata_url_path, sender=model)
            post_save.connect(self.check_metadata_language, sender=model)

            sites_field_class = model_metadata.sites_field_class(model)
            if sites_field_class is ManyToManyField:
                through_model = getattr(
                    model, model_metadata.sites_field_name).through
                m2m_changed.connect(
                    self.check_metadata_sites, sender=through_model)
            else:
                post_save.connect(self.check_metadata_site, sender=model)

    def delete_metadata(self, sender, **kwargs):
        Metadata.objects.filter_by_content_object(kwargs['instance']).delete()

    def check_metadata_url_path(self, sender, **kwargs):
        instance = kwargs['instance']
        model_metadata = self._registry.get(sender)
        if model_metadata:
            try:
                metadata = Metadata.objects.get_for_content_object(instance)
            except Metadata.DoesNotExist:
                pass
            else:
                metadata.update_url_path()

    def check_metadata_language(self, sender, **kwargs):
        instance = kwargs['instance']
        model_metadata = self._registry.get(sender)
        if model_metadata:
            try:
                metadata = Metadata.objects.get_for_content_object(instance)
            except Metadata.DoesNotExist:
                pass
            else:
                metadata.update_language()

    def check_metatag_site(self, sender, **kwargs):
        instance = kwargs['instance']
        model_metadata = self._registry.get(sender)
        if model_metadata:
            try:
                metadata = Metadata.objects.get_for_content_object(instance)
            except Metadata.DoesNotExist:
                pass
            else:
                metadata.update_sites()

    def check_metatag_sites(self, sender, **kwargs):
        instance = kwargs['instance']
        action = kwargs['action']
        model_metadata = self._registry.get(instance.__class__)
        actions = ('post_add', 'post_remove', 'post_clear')
        if model_metadata and action in actions:
            try:
                metadata = Metadata.objects.get_for_content_object(instance)
            except Metadata.DoesNotExist:
                pass
            else:
                metadata.update_sites()


site = MetadataSite()
