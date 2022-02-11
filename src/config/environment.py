import os


def _get_bool(variable: str, default: bool = False) -> bool:
    value = os.getenv(variable)
    return default if value is None else value.lower() in ('true', '1', 'yes')


# TODO make method for getting first existing env in a list
TOKEN = os.getenv('TOKEN')

USE_WEBHOOKS = _get_bool('USE_WEBHOOKS')
APP_URL = os.getenv('APP_URL', os.getenv('WEBHOOK_URL'))
USE_PROXY = _get_bool('USE_PROXY')
PORT = int(os.environ.get('PORT', '8443'))

DATABASE_URL = os.getenv('DB_URL', os.getenv('DATABASE_URL', 'sqlite:///development.db'))
PG_SCHEMA = os.getenv('PG_SCHEMA', 'public')
REDIS_URL = os.getenv('REDIS_TLS_URL', os.getenv('REDIS_URL', 'redis://localhost'))

REFRESH_AT_STARTUP = _get_bool('REFRESH_AT_STARTUP', True)
DEBUG = _get_bool('DEBUG')
