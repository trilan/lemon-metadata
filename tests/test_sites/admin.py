import lemon
from .models import Article, Forum


lemon.site.register(Article,
    list_display=('title', 'content'),
)

lemon.site.register(Forum,
    list_display=('name', 'description'),
)
