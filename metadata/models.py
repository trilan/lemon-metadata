from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _

from .managers import MetadataManager


LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)


class Metadata(models.Model):

    url_path = models.CharField(
        verbose_name=_('URL path'),
        max_length=255,
        db_index=True,
    )
    sites = models.ManyToManyField(
        to=Site,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_(u'sites'),
    )
    language = models.CharField(
        verbose_name=_(u'language'),
        max_length=10,
        db_index=True,
        choices=LANGUAGES,
        default=get_language,
    )

    title = models.CharField(
        verbose_name=_(u'page title'),
        max_length=255,
        blank=True,
        help_text=_(u'Displayed in browser window title.'),
    )
    title_extend = models.BooleanField(
        verbose_name=_(u'extend page title with site name'),
        default=True,
        help_text=_(u'For example, <strong>Page title - Site name</strong>'),
    )
    keywords = models.TextField(
        verbose_name=_(u'page keywords'),
        blank=True,
        help_text=_(
            u'Keywords are terms describing web page content and used '
            u'by search engines. Here you can enumerate some words '
            u'divided by commas.'
        ),
    )
    description = models.TextField(
        verbose_name=_(u'page description'),
        blank=True,
        help_text=_(
            u'Here you can set short description of this page '
            u'for search engines.'
        ),
    )

    enabled = models.BooleanField(
        verbose_name=_(u'enabled'),
        default=False,
        help_text=_(u'If not set, meta tags will not be used on page.'),
    )

    content_type = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = MetadataManager()

    class Meta:
        verbose_name = _(u'page metadata')
        verbose_name_plural = _(u'pages metadata')

    def __unicode__(self):
        return self.url_path
