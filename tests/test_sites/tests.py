from django.test import TestCase

from metadata import MetadataSite
from .models import Article, Person


class MetadataSiteTests(TestCase):

    def setUp(self):
        self.site = MetadataSite()
        self.site.register(Article)

    def tearDown(self):
        for model in list(self.site._registry):
            self.site.unregister(model)

    def test_registers_model(self):
        self.assertIn(Article, self.site._registry)

    def test_unregisters_model(self):
        article_metadata = self.site._registry[Article]
        self.site.unregister(Article)
        self.assertNotIn(Article, self.site._registry)
        self.assertFalse(article_metadata._enabled)
