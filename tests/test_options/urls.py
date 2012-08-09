from django.conf.urls import patterns, url
from django.views.generic import DetailView
from .models import Article, Forum


urlpatterns = patterns('',
    url(r'^articles/(?P<pk>\d+)/$',
        DetailView.as_view(model=Article),
        name='article_detail'),
    url(r'^forums/(?P<pk>\d+)/$',
        DetailView.as_view(model=Forum),
        name='forum_detail'),
)
