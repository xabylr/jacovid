import os

def get_bool(variable, default: bool = False) -> bool:
    result = os.getenv(variable)
    if result is None:
        return default
    else:
        return result.lower() in ('true', '1', 'yes')