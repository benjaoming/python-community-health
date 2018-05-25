from .base import *

try:
    from .local import *
except ImportError:
    print(
        "To sync data from Github API, add a project/settings/local.py with "
        "these kind of these contents:\n\n"
        "GITHUB_USERNAME = 'lsldsjfsfsf'\n"
        "GITHUB_PASSWORD = 'lsldsjfsfsf'"
    )
