from django.contrib import admin as django_admin
from django.test import TestCase

from lemon import extradmin as lemon_admin
from lemon.extradmin import ModelAdmin

from metadata.admin import MetadataAdmin
from metadata.models import Metadata


class MetadataAdminTests(TestCase):

    def test_class(self):
        self.assertTrue(issubclass(MetadataAdmin, ModelAdmin))


class AdminSiteTests(TestCase):

    def test_metadata_isnt_registered_in_django(self):
        self.assertNotIn(Metadata, django_admin.site._registry)

    def test_metadata_is_registered_in_lemon(self):
        self.assertIsInstance(lemon_admin.site._registry[Metadata], MetadataAdmin)
