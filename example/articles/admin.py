import metadata
from lemon import extradmin
from .models import Article


extradmin.site.register(Article)
metadata.site.register(Article, sites_field_name='sites')
