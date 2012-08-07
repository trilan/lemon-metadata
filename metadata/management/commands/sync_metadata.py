# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand

from lemon import extradmin

from metadata import site
from metadata.models import Metadata


class Command(NoArgsCommand):

    help = 'Sync metadata with all registered models'

    def handle_noargs(self, **options):
        print 'Starting metadata synchronisation with all registered models.'
        extradmin.autodiscover()
        for model, metadata in site._registry.items():
            print 'Syncing %s.%s model.' % (model._meta.app_label, model.__name__)
            self.sync_metadata(model, metadata)
        print 'All objects with `get_absolute_url` method was synced.',
        print 'Removing orphaned metadata.'
        self.remove_orphaned()
        print 'Done.'

    def sync_metadata(self, model, metadata):
        for obj in model.objects.all():
            try:
                metadata = Metadata.objects.get_for_content_object(obj)
            except Metadata.DoesNotExist:
                pass
            else:
                metadata.update_url_path()
                metadata.update_language()
                metadata.update_sites()
                sites = ', '.join([s.domain for s in metadata.sites.all()])
                print '  Metadata for %s (%s) was updated.' % (
                    metadata.url_path,
                    sites,
                )

    def remove_orphaned(self):
        for metadata in Metadata.objects.all():
            if metadata.content_type and metadata.object_id:
                if not metadata.content_object:
                    sites = ', '.join([s.domain for s in metadata.sites.all()])
                    print '  Metadata for %s (%s) was deleted.' % (
                        metadata.url_path,
                        sites,
                    )
                    metadata.delete()
