import os

def _get_bool(variable: str, default: bool = False) -> bool:
    value = os.getenv(variable)
    return default if value is None else value.lower() in ('true', '1', 'yes')

#TODO make method for getting first existing env in a list

USE_PROXY = _get_bool('USE_PROXY')
USE_WEBHOOKS = _get_bool('USE_WEBHOOKS', True)
TOKEN = os.getenv('TOKEN')
APP_URL = os.getenv('APP_URL')
DATABASE_URL = os.getenv('DB_URL', os.getenv('DATABASE_URL', 'sqlite:///development.db'))
PG_SCHEMA = os.getenv('PG_SCHEMA', 'public')
REDIS_URL = os.getenv('REDIS_TLS_URL', os.getenv('REDIS_URL', 'redis://localhost'))
PORT = int(os.environ.get('PORT', '8443'))  # Port is given by Heroku
REFRESH_AT_STARTUP = _get_bool('REFRESH_AT_STARTUP', True)
DEBUG = _get_bool('DEBUG', False)