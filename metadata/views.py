from django.template.response import TemplateResponse
from django.utils import translation

from .models import Metadata
from .utils import get_site_id


def sitemap_xml(request):
    translation.activate('en')
    site_id = get_site_id(request)
    queryset = Metadata.objects.filter(sites=site_id, enabled=True)
    return TemplateResponse(request, 'metadata/sitemap.xml', {
        'object_list': queryset,
    }, content_type='application/xml')
