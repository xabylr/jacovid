import os


def get_bool(variable: str, default: bool = False) -> bool:
    value = os.getenv(variable)
    return default if value is None else value.lower() in ('true', '1', 'yes')
