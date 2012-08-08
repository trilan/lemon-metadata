from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return self.title


class Forum(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Person(models.Model):

    fullname = models.CharField(max_length=100)
    bio = models.TextField()

    def __unicode__(self):
        return self.fullname
