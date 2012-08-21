import lemon
import metadata
from .models import Article


class ArticleAdmin(metadata.MetadataAdminMixin, lemon.ModelAdmin):
    pass


lemon.site.register(Article, ArticleAdmin)
metadata.site.register(Article, sites_field_name='sites')
