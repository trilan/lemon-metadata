from django.contrib import admin
from django.test import TestCase

from metadata import MetadataSite
from metadata.sites import NotRegisteredInAdmin

from .models import Article, Person


admin.autodiscover()


class MetadataSiteTests(TestCase):

    def setUp(self):
        self.site = MetadataSite()

    def test_registers_model(self):
        self.site.register(Article)
        self.assertIn(Article, self.site._registry)

    def test_raises_exception_if_model_isnt_registered_in_admin(self):
        with self.assertRaises(NotRegisteredInAdmin):
            self.site.register(Person)
