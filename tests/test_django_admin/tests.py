import lemon

from django.contrib import admin as django_admin
from django.test import TestCase

from metadata.admin import MetadataAdmin
from metadata.models import Metadata


class MetadataAdminTests(TestCase):

    def test_class(self):
        self.assertFalse(issubclass(MetadataAdmin, lemon.ModelAdmin))


class AdminSiteTests(TestCase):

    def test_metadata_is_registered_in_django(self):
        self.assertIsInstance(django_admin.site._registry[Metadata], MetadataAdmin)

    def test_metadata_isnt_registered_in_lemon(self):
        self.assertNotIn(Metadata, lemon.site._registry)
