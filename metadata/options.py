from django.contrib.sites.models import Site
from django.db.models import FieldDoesNotExist, ForeignKey, ManyToManyField
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.utils.translation import get_language

from .models import Metadata


class ModelMetadata(object):

    language_field_name = None
    sites_field_name = None

    def __init__(self, model, **options):
        self.model = model
        for name, value in options.items():
            setattr(self, name, value)
        self._enabled = False

    def _connect_signal_handlers(self):
        post_save.connect(self.handle_object_update, sender=self.model)
        pre_delete.connect(self.handle_object_deletion, sender=self.model)

        sites_field_class = self.sites_field_class()
        if sites_field_class is ManyToManyField:
            self._through = getattr(self.model, self.sites_field_name).through
            m2m_changed.connect(self.handle_object_update, self._through)

    def _disconnect_signal_handlers(self):
        post_save.disconnect(self.handle_object_update, sender=self.model)
        pre_delete.disconnect(self.handle_object_deletion, sender=self.model)
        if hasattr(self, '_through'):
            m2m_changed.disconnect(self.handle_object_update, self._through)

    def enable(self):
        if not self._enabled:
            self._connect_signal_handlers()
            self._enabled = True

    def disable(self):
        if self._enabled:
            self._disconnect_signal_handlers()
            self._enabled = False

    def sites_field_class(self):
        try:
            return self.model._meta.get_field_by_name(
                self.sites_field_name)[0].__class__
        except FieldDoesNotExist:
            return None

    def language(self, obj):
        if not self.language_field_name:
            return get_language()
        return getattr(obj, self.language_field_name)

    def sites(self, obj):
        if not self.sites_field_name:
            return Site.objects.all()
        sites_field_class = self.sites_field_class()
        if sites_field_class is ForeignKey:
            return [getattr(obj, self.sites_field_name)]
        if sites_field_class is ManyToManyField:
            return getattr(obj, self.sites_field_name).all()
        return []

    def url_path(self, obj):
        try:
            return obj.get_absolute_url()
        except Exception:
            return None

    def handle_object_update(self, sender, **kwargs):
        raw = kwargs.get('raw')
        action = kwargs.get('action', 'post_save')
        actions = ('post_add', 'post_remove', 'post_clear', 'post_save')
        if raw or action not in actions:
            return

        instance = kwargs['instance']
        try:
            metadata = Metadata.objects.get_for_content_object(instance)
        except Metadata.DoesNotExist:
            if action != 'post_save':
                # If instance isn't created or changed directly, skip metadata
                # creation.
                return
            metadata = Metadata(content_object=instance)
        self.update_metadata(metadata)

    def handle_object_deletion(self, sender, **kwargs):
        instance = kwargs['instance']
        try:
            metadata = Metadata.objects.get_for_content_object(instance)
        except Metadata.DoesNotExist:
            return
        self.delete_metadata(metadata)

    def update_metadata(self, metadata):
        obj = metadata.content_object

        metadata.url_path = self.url_path(obj)
        metadata.language = self.language(obj)
        metadata.save()

        metadata.sites.clear()
        metadata.sites.add(*self.sites(obj))

    def delete_metadata(self, metadata):
        metadata.delete()
