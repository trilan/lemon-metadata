from .settings import *


ROOT_URLCONF = 'tests.test_lemon_admin.urls'

INSTALLED_APPS = (
    'lemon',
) + INSTALLED_APPS + (
    'tests.test_lemon_admin',
)
