# -*- coding: UTF-8 -*-

from django.conf import settings


CONFIG = {
    'TITLE_SEPARATOR': u' — ',
    'TITLE_REVERSED': False,
}
CONFIG.update(getattr(settings, 'METADATA_CONFIG', {}))
TITLE_SEPARATOR = getattr(settings, 'METADATA_TITLE_SEPARATOR', u' — ')
TITLE_REVERSED = getattr(settings, 'METADATA_TITLE_REVERSED', False)
