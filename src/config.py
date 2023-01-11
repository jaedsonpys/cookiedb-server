import os
from pathlib import Path

HOME_USER = Path.home()
COOKIEDB_PATH = os.path.join(HOME_USER, '.cookiedbserver')


def check_config():
    return os.path.isdir(COOKIEDB_PATH)
