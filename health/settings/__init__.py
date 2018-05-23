from .base import *

try:
    from .local import *
except ImportError:
    raise RuntimeError(
        "Add a health/settings/local.py with these kind of these "
        "contents:\n\n"
        "GITHUB_USERNAME = 'lsldsjfsfsf'\n"
        "GITHUB_PASSWORD = 'lsldsjfsfsf'"
    )
