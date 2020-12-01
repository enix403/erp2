from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / 'base' / 'settings' / 'environs' / '.tablenew.env'
load_dotenv(dotenv_path=env_path)


if os.getenv('APP_DEBUG') == 'true':
    from .settings_dev import *
else:
    from .settings_prod import *
