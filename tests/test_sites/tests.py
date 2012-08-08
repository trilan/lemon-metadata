from django.contrib import admin
from django.test import TestCase

from metadata import MetadataSite
from metadata.sites import NotRegisteredInAdmin

from .models import Article, Forum, Person


admin.autodiscover()


class MetadataSiteTests(TestCase):

    def setUp(self):
        self.site = MetadataSite()

    def test_registers_model(self):
        self.site.register(Article)
        self.assertIn(Article, self.site._registry)

    def test_registers_model_list(self):
        self.site.register((Article, Forum))
        self.assertIn(Article, self.site._registry)
        self.assertIn(Forum, self.site._registry)

    def test_raises_exception_if_model_isnt_registered_in_admin(self):
        with self.assertRaises(NotRegisteredInAdmin):
            self.site.register(Person)
