from django.utils.functional import SimpleLazyObject
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from .models import Metadata
from .settings import CONFIG


class MetadataContextObject(object):

    def __init__(self, url_path, site):
        metadata = self._get_metadata(url_path, site)
        if metadata and metadata.enabled:
            self.title = self._get_title(metadata, site)
            self.keywords = metadata.keywords
            self.description = metadata.description
            self.enabled = True
        else:
            self.title = self.keywords = self.description = ''
            self.enabled = False

    def _get_metadata(self, url_path, site):
        queryset = Metadata.objects.filter(
            url_path=url_path,
            language=get_language(),
            sites=site,
            enabled=True,
        )
        try:
            return queryset[0]
        except IndexError:
            return None

    def _get_title(self, metadata, site):
        if not metadata.title:
            return ''
        titles = [metadata.title]
        if metadata.title_extend:
            titles.append(site.name)
        if CONFIG['TITLE_REVERSED']:
            titles.reverse()
        return mark_safe(CONFIG['TITLE_SEPARATOR'].join(titles))


def metadata(request):
    return {
        'metadata': SimpleLazyObject(
            lambda: MetadataContextObject(request.path, request.site)
        )
    }
