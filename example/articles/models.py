from django.contrib.sites.models import Site
from django.db import models


class Article(models.Model):

    sites = models.ManyToManyField(Site)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('articles_article_detail', (), {'pk': self.pk})
