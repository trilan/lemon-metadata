import lemon
from django.contrib import admin
from tests.urls import urlpatterns


admin.autodiscover()
urlpatterns += patterns('',
    url(r'^admin/', include(lemon.site.urls)),
)
