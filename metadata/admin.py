from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin

from .models import Metadata
from .widgets import AdminSmallTextareaWidget


class MetadataAdminMixin(object):

    change_form_template = 'metadata/admin/change_form.html'


class MetadataAdmin(extradmin.ModelAdmin):

    list_display = (
        'url_path', 'title', 'changefreq', 'lastmod', 'language', 'enabled',
    )
    list_display_links = ('url_path', 'title')
    list_filter = ('enabled', 'lastmod')
    formfield_overrides = {
        models.TextField: {'widget': AdminSmallTextareaWidget},
    }
    string_overrides = {
        'add_title': _(u'Add metadata for page'),
        'change_title': _(u'Change metadata for page'),
        'changelist_title': _(u'Choose metadata to change'),
        'changelist_popup_title': _(u'Choose metadata'),
        'changelist_addlink_title': _(u'Add metadata'),
        'changelist_paginator_description': lambda n: ungettext(
            '%(count)d page has metadata', '%(count)d pages have metadata', n
        ),
    }


extradmin.site.register(Metadata, MetadataAdmin)
