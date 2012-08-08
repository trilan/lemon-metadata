from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import translation

from metadata.options import ModelMetadata
from .models import Article, Forum


def create_site(**kwargs):
    defaults = {'name': 'example.com', 'domain': 'example.com'}
    defaults.update(kwargs)
    return Site.objects.create(**defaults)


def create_article(**kwargs):
    defaults = {'title': 'title', 'content': 'content', 'language': 'en'}
    defaults.update(kwargs)
    return Article.objects.create(**defaults)


def create_forum(**kwargs):
    sites = kwargs.pop('sites', [])
    defaults = {'name': 'name', 'description': 'description', 'language': 'en'}
    defaults.update(kwargs)
    forum = Forum.objects.create(**defaults)
    if sites:
        forum.sites.add(*sites)
    return forum


class DefaultModelMetadataTests(TestCase):

    def setUp(self):
        self.default_site = Site.objects.get(id=1)
        self.custom_site = create_site()
        self.article = create_article(language='ru')
        self.model_metadata = ModelMetadata()

    def test_returns_current_language(self):
        with translation.override('en'):
            language = self.model_metadata.language(self.article)
        self.assertEqual(language, 'en')

    def test_returns_all_sites(self):
        sites = self.model_metadata.sites(self.article)
        self.assertItemsEqual(sites, [self.default_site, self.custom_site])


class FilledModelMetadataTests(TestCase):

    def setUp(self):
        self.site1 = create_site()
        self.site2 = create_site()

        self.article = create_article(language='ru', site=self.site1)
        self.forum = create_forum(language='ru', sites=[self.site1, self.site2])

        self.model_metadata = ModelMetadata()
        self.model_metadata.language_field_name = 'language'
        self.model_metadata.sites_field_name = 'site'

    def test_returns_object_language(self):
        with translation.override('en'):
            language = self.model_metadata.language(self.article)
        self.assertEqual(language, 'ru')

    def test_returns_object_site(self):
        sites = self.model_metadata.sites(self.article)
        self.assertItemsEqual(sites, [self.site1])

    def test_returns_object_sites(self):
        self.model_metadata.sites_field_name = 'sites'
        sites = self.model_metadata.sites(self.forum)
        self.assertItemsEqual(sites, [self.site1, self.site2])

    def test_returns_empty_list_of_sites_if_field_name_is_wrong(self):
        self.model_metadata.sites_field_name = 'abcdef'
        sites = self.model_metadata.sites(self.forum)
        self.assertEqual(sites, [])

    def test_returns_empty_list_of_sites_if_field_type_is_wrong(self):
        self.model_metadata.sites_field_name = 'name'
        sites = self.model_metadata.sites(self.forum)
        self.assertEqual(sites, [])

    def test_returns_object_url_path(self):
        url_path = self.model_metadata.url_path(self.article)
        self.assertEqual(url_path, '/articles/{0}/'.format(self.article.pk))

    def test_returns_none_if_object_has_no_absolute_url(self):
        url_path = self.model_metadata.url_path(self.forum)
        self.assertIsNone(url_path)
