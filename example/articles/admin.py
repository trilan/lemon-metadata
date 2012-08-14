import metadata
from lemon import extradmin
from .models import Article


class ArticleAdmin(metadata.MetadataAdminMixin, extradmin.ModelAdmin):
    pass


extradmin.site.register(Article, ArticleAdmin)
metadata.site.register(Article, sites_field_name='sites')
