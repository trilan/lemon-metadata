from django.test import TestCase

from metadata import MetadataSite
from .models import Article, Person


class MetadataSiteTests(TestCase):

    def setUp(self):
        self.site = MetadataSite()

    def test_registers_model(self):
        self.site.register(Article)
        self.assertIn(Article, self.site._registry)
