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
        self._connect_signal_handlers()

    def _connect_signal_handlers(self):
        pre_delete.connect(self.delete_metadata, sender=self.model)
        post_save.connect(self.check_metadata_url_path, sender=self.model)
        post_save.connect(self.check_metadata_language, sender=self.model)

        sites_field_class = self.sites_field_class()
        if sites_field_class is ManyToManyField:
            through = getattr(self.model, self.sites_field_name).through
            m2m_changed.connect(self.check_metadata_sites, sender=through)
        elif sites_field_class is ForeignKey:
            post_save.connect(self.check_metadata_site, sender=self.model)

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

    def delete_metadata(self, sender, **kwargs):
        Metadata.objects.filter_by_content_object(kwargs['instance']).delete()

    def check_metadata_url_path(self, sender, **kwargs):
        instance = kwargs['instance']
        try:
            metadata = Metadata.objects.get_for_content_object(instance)
        except Metadata.DoesNotExist:
            return
        metadata.update_url_path()

    def check_metadata_language(self, sender, **kwargs):
        instance = kwargs['instance']
        try:
            metadata = Metadata.objects.get_for_content_object(instance)
        except Metadata.DoesNotExist:
            return
        metadata.update_language()

    def check_metadata_site(self, sender, **kwargs):
        instance = kwargs['instance']
        try:
            metadata = Metadata.objects.get_for_content_object(instance)
        except Metadata.DoesNotExist:
            return
        metadata.update_sites()

    def check_metadata_sites(self, sender, **kwargs):
        instance = kwargs['instance']
        if kwargs['action'] in ('post_add', 'post_remove', 'post_clear'):
            try:
                metadata = Metadata.objects.get_for_content_object(instance)
            except Metadata.DoesNotExist:
                return
            metadata.update_sites()
