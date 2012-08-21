from operator import attrgetter

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, RequestFactory

from metadata.models import Metadata
from metadata.views import sitemap_xml


def create_request(site=None):
    request_factory = RequestFactory()
    request = request_factory.get('/sitemap.xml')
    if site is not None:
        request.site = site
    return request


def create_metadata(**kwargs):
    sites = kwargs.pop('sites', [])
    metadata = Metadata.objects.create(**kwargs)
    metadata.sites.add(*sites)
    return metadata


class SitemapXMLTestCase(TestCase):

    def setUp(self):
        self.site1 = Site.objects.get(id=1)
        self.site2 = Site.objects.create(
            domain='s2.example.com',
            name='s2.example.com',
        )
        self.metadata1 = create_metadata(
            url_path='/',
            language='en',
            sites=[self.site1],
        )
        self.metadata2 = create_metadata(
            url_path='/about/',
            language='ru',
            sites=[self.site1],
        )

    def test_has_proper_content_type(self):
        response = sitemap_xml(create_request(site=self.site1))
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_object_list_contains_metadata(self):
        response = sitemap_xml(create_request(site=self.site1))
        self.assertQuerysetEqual(response.context_data['object_list'], [
            '/',
            '/about/'
        ], transform=attrgetter('url_path'), ordered=False)

    def test_object_list_is_empty_if_no_metadata(self):
        response = sitemap_xml(create_request(site=self.site2))
        self.assertQuerysetEqual(response.context_data['object_list'], [])
