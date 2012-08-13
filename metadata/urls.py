from django.conf.urls import patterns, url
from .views import sitemap_xml


urlpatterns = patterns('',
    url(r'^$', sitemap_xml, name='sitemap_xml'),
)
