import os
import cookiedb
from .config import DATABASES_PATH
from .config import PASSWORD_PATH


def _get_key() -> str:
    with open(PASSWORD_PATH, 'r') as file:
        key = file.read()

    return key


def list_databases() -> list:
    db_files = os.listdir(DATABASES_PATH)
    db_files = [f.replace('.cookiedb', '') for f in db_files]
    return db_files
