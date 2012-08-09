from django.contrib.sites.models import Site
from django.db import models


class Article(models.Model):

    site = models.ForeignKey(Site, null=True)
    language = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), {'pk': self.pk})


class Forum(models.Model):

    sites = models.ManyToManyField(Site)
    language = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum_detail', (), {'pk': self.pk})
