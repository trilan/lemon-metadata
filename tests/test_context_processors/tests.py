# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.test import TestCase, RequestFactory
from django.utils import translation

from metadata.context_processors import metadata
from metadata.models import Metadata


def create_request(*args, **kwargs):
    site = kwargs.get('site', Site.objects.get(pk=1))
    request_factory = RequestFactory()
    request = request_factory.get(*args, **kwargs)
    request.site = site
    return request


def create_site(**kwargs):
    defaults = {'name': 'example.com', 'domain': 'example.com'}
    defaults.update(kwargs)
    return Site.objects.create(**defaults)


def create_metadata(**kwargs):
    sites = kwargs.get('sites')
    if sites is None:
        sites = Site.objects.all()
    defaults = dict(
        language='en',
        title='title',
        keywords='keywords',
        description='description',
        enabled=True,
    )
    defaults.update(kwargs)
    metadata = Metadata.objects.create(**defaults)
    metadata.sites.add(*sites)
    return metadata


class MetadataContextProcessorTests(TestCase):

    def assertMetadataIsEmpty(self, obj):
        self.assertFalse(obj.enabled)
        self.assertEqual(obj.title, '')
        self.assertEqual(obj.keywords, '')
        self.assertEqual(obj.description, '')

    def assertMetadataIsPresent(self, obj):
        self.assertTrue(obj.enabled)
        self.assertEqual(obj.title, u'title — example.com')
        self.assertEqual(obj.keywords, 'keywords')
        self.assertEqual(obj.description, 'description')

    def test_metadata_object_is_lazy(self):
        request = create_request('/')
        with self.assertNumQueries(0):
            metadata(request)

    def test_metadata_is_empty_if_does_not_exist(self):
        context = metadata(create_request('/'))
        self.assertMetadataIsEmpty(context['metadata'])

    def test_metadata_is_empty_if_disabled(self):
        create_metadata(url_path='/', enabled=False)
        context = metadata(create_request('/'))
        self.assertMetadataIsEmpty(context['metadata'])

    def test_metadata_is_present_if_enabled(self):
        create_metadata(url_path='/')
        context = metadata(create_request('/'))
        with translation.override('en'):
            self.assertMetadataIsPresent(context['metadata'])

    def test_metadata_is_empty_if_site_doesnt_match(self):
        create_metadata(url_path='/')
        context = metadata(create_request('/', site=create_site()))
        with translation.override('en'):
            self.assertMetadataIsEmpty(context['metadata'])

    def test_metadata_is_empty_if_language_doesnt_match(self):
        create_metadata(url_path='/')
        context = metadata(create_request('/'))
        with translation.override('ru'):
            self.assertMetadataIsEmpty(context['metadata'])

    def test_metadata_is_empty_if_url_path_doesnt_match(self):
        create_metadata(url_path='/about/')
        context = metadata(create_request('/'))
        with translation.override('en'):
            self.assertMetadataIsEmpty(context['metadata'])

    def test_empty_metadata_title_is_not_extended(self):
        create_metadata(url_path='/', title='', title_extend=True)
        context = metadata(create_request('/'))
        with translation.override('en'):
            self.assertEqual(context['metadata'].title, '')
