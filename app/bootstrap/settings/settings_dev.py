# pylint: disable=unused-wildcard-import
from .settings_common import *


INSTALLED_APPS.extend([
    'debug_toolbar',
    'django_extensions',
])

MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: True,
}

TEMPLATE_DEBUG = True

# st_dist_dir = BASE_DIR / 'salary' / 'frontend' / 'dist' / 'static'
# st_build_dir = BASE_DIR / 'salary' / 'frontend' / 'build' / 'static'
# STATICFILES_DIRS = tuple(d for d in [st_dist_dir, st_build_dir] if d.is_dir())

SHELL_PLUS = "plain"

HTML_MINIFY = True
# HTML_MINIFY = False
