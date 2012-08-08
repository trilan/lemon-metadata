from lemon import extradmin
from .models import Article, Forum


extradmin.site.register(Article,
    list_display=('title', 'content'),
)

extradmin.site.register(Forum,
    list_display=('name', 'description'),
)
