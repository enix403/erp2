import os
from dotenv import load_dotenv
from app.base.fileresolver import resolve_root

env_path = resolve_root('config/environs/.hrcupdate.env')
load_dotenv(dotenv_path=env_path)

if os.getenv('APP_DEBUG') == 'true':
    from .settings_dev import *
else:
    from .settings_prod import *
