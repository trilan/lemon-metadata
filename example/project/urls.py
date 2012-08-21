import lemon

from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^articles/', include('articles.urls')),
    url(r'^admin/', include(lemon.site.urls)),
    url(r'^sitemap\.xml$', include('metadata.urls')),
)
