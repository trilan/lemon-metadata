from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from .models import Metadata
from .widgets import AdminSmallTextareaWidget


if 'lemon' in settings.INSTALLED_APPS:
    import lemon as admin
    CHANGE_FORM_TEMPLATE = 'metadata/lemon/change_form.html'
else:
    from django.contrib import admin
    CHANGE_FORM_TEMPLATE = 'metadata/admin/change_form.html'


class MetadataAdminMixin(object):

    change_form_template = CHANGE_FORM_TEMPLATE


class MetadataModelAdmin(MetadataAdminMixin, admin.ModelAdmin):
    pass


class MetadataAdmin(admin.ModelAdmin):

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


admin.site.register(Metadata, MetadataAdmin)
