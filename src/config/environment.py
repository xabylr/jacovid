import os

def _get_bool(variable: str, default: bool = False) -> bool:
    value = os.getenv(variable)
    return default if value is None else value.lower() in ('true', '1', 'yes')

USE_PROXY = _get_bool('USE_PROXY')
USE_WEBHOOKS = _get_bool('USE_WEBHOOKS', True)
TOKEN = os.getenv('TOKEN')
APP_URL = os.getenv('APP_URL')
DB_URL = os.environ.get('DB_URL', f'sqlite:///development.db')
PG_SCHEMA = os.environ.get('PG_SCHEMA', 'public')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost')
PORT = int(os.environ.get('PORT', '8443'))  # Port is given by Heroku
DEBUG = _get_bool('DEBUG', False)