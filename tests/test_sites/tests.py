from mock import patch, call
from django.test import TestCase

from metadata import MetadataSite
from .models import Article, Person


class MetadataSiteTests(TestCase):

    def setUp(self):
        self.site = MetadataSite()
        self.site.register(Article)
        self.site.register(Person)

    def tearDown(self):
        self.site.unregister_all()

    def test_registers_model(self):
        self.assertIn(Article, self.site._registry)

    def test_unregisters_model(self):
        article_metadata = self.site._registry[Article]
        self.site.unregister(Article)
        self.assertNotIn(Article, self.site._registry)
        self.assertFalse(article_metadata._enabled)

    @patch.object(MetadataSite, 'unregister')
    def test_unregisters_all_models(self, unregister):
        self.site.unregister_all()
        self.assertEqual(unregister.call_count, 2)
        unregister.assert_has_calls([call(Article), call(Person)], any_order=True)
