# pylint: disable=unused-wildcard-import
from .settings_common import *


st_build_dir = BASE_DIR / 'salary' / 'frontend' / 'build' / 'static'

STATICFILES_DIRS = tuple(d for d in [st_build_dir] if d.is_dir())
