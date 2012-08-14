from django.contrib import admin
from lemon import extradmin
from tests.urls import urlpatterns


admin.autodiscover()
urlpatterns += patterns('',
    url(r'^admin/', include(extradmin.site.urls)),
)
