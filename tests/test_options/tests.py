from mock import patch

from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import translation

from metadata.options import ModelMetadata
from metadata.models import Metadata

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
        self.article_metadata = ModelMetadata(Article)
        self.article_metadata.enable()

    def tearDown(self):
        self.article_metadata.disable()

    def test_returns_current_language(self):
        with translation.override('en'):
            language = self.article_metadata.language(self.article)
        self.assertEqual(language, 'en')

    def test_returns_all_sites(self):
        sites = self.article_metadata.sites(self.article)
        self.assertEqual(len(sites), 2)
        self.assertIn(self.default_site, sites)
        self.assertIn(self.custom_site, sites)


class FilledModelMetadataTests(TestCase):

    def setUp(self):
        self.site1 = create_site()
        self.site2 = create_site()

        self.article = create_article(language='ru', site=self.site1)
        self.forum = create_forum(language='ru', sites=[self.site1, self.site2])

        self.article_metadata = ModelMetadata(Article,
            language_field_name='language',
            sites_field_name='site',
        )
        self.article_metadata.enable()

        self.forum_metadata = ModelMetadata(Forum,
            language_field_name='language',
            sites_field_name='sites',
        )
        self.forum_metadata.enable()

    def tearDown(self):
        self.article_metadata.disable()
        self.forum_metadata.disable()

    def test_returns_object_language(self):
        with translation.override('en'):
            language = self.article_metadata.language(self.article)
        self.assertEqual(language, 'ru')

    def test_returns_object_site(self):
        sites = self.article_metadata.sites(self.article)
        self.assertEqual(len(sites), 1)
        self.assertIn(self.site1, sites)

    def test_returns_object_sites(self):
        sites = self.forum_metadata.sites(self.forum)
        self.assertEqual(len(sites), 2)
        self.assertIn(self.site1, sites)
        self.assertIn(self.site2, sites)

    def test_returns_empty_list_of_sites_if_field_name_is_wrong(self):
        self.forum_metadata.sites_field_name = 'abcdef'
        sites = self.forum_metadata.sites(self.forum)
        self.assertEqual(sites, [])

    def test_returns_empty_list_of_sites_if_field_type_is_wrong(self):
        self.forum_metadata.sites_field_name = 'name'
        sites = self.forum_metadata.sites(self.forum)
        self.assertEqual(sites, [])

    def test_returns_object_url_path(self):
        url_path = self.article_metadata.url_path(self.article)
        self.assertEqual(url_path, '/articles/{0}/'.format(self.article.pk))


class ModelMetadataUpdateTests(TestCase):

    def setUp(self):
        self.site1 = create_site()
        self.site2 = create_site()
        self.forum = create_forum(language='ru', sites=[self.site1, self.site2])
        self.metadata = Metadata(content_object=self.forum)
        self.forum_metadata = ModelMetadata(Forum,
            sites_field_name='sites',
            language_field_name='language',
        )
        self.forum_metadata.update_metadata(self.metadata)

    def test_creates_metadata(self):
        self.assertIsNotNone(self.metadata)
        self.assertEqual(self.metadata.url_path, '/forums/1/')
        self.assertEqual(self.metadata.language, 'ru')

        sites = self.metadata.sites.all()
        self.assertEqual(len(sites), 2)
        self.assertIn(self.site1, sites)
        self.assertIn(self.site2, sites)

    def test_updates_metadata(self):
        self.forum.language = 'en'
        self.forum.sites.remove(self.site2)
        self.forum.save()
        metadata = Metadata.objects.get_for_content_object(self.forum)
        self.forum_metadata.update_metadata(metadata)
        self.assertEqual(metadata.language, 'en')
        self.assertEqual(list(metadata.sites.all()), [self.site1])


class ModelMetadataSignalHandlersTests(TestCase):

    def setUp(self):
        self.article_metadata = ModelMetadata(Article)
        self.article_metadata.enable()
        self.forum_metadata = ModelMetadata(Forum, sites_field_name='sites')
        self.forum_metadata.enable()

    def tearDown(self):
        self.article_metadata.disable()
        self.forum_metadata.disable()

    @patch.object(ModelMetadata, 'update_metadata')
    def test_metadata_created_on_object_creation(self, update_metadata):
        article = create_article()
        self.assertEqual(update_metadata.call_count, 1)
        self.assertEqual(update_metadata.call_args[0][0].content_object, article)

    def test_metadata_updated_on_object_update(self):
        article = create_article()
        metadata = Metadata.objects.get_for_content_object(article)
        with patch.object(ModelMetadata, 'update_metadata') as update_metadata:
            article.save()
            update_metadata.assert_called_once_with(metadata)

    def test_metadata_updated_if_sites_changed(self):
        forum = create_forum()
        metadata = Metadata.objects.get_for_content_object(forum)
        with patch.object(ModelMetadata, 'update_metadata') as update_metadata:
            forum.sites.add(create_site())
            update_metadata.assert_called_once_with(metadata)

    def test_metadata_deleted_on_object_deletion(self):
        article = create_article()
        metadata = Metadata.objects.get_for_content_object(article)
        with patch.object(ModelMetadata, 'delete_metadata') as delete_metadata:
            article.delete()
            delete_metadata.assert_called_once_with(metadata)
