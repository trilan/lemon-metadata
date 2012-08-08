from lemon import extradmin
from .models import Article


extradmin.site.register(Article,
    list_display=('title', 'content'),
)
