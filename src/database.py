import os
from .config import DATABASES_PATH


def list_databases() -> list:
    db_files = os.listdir(DATABASES_PATH)
    db_files = [f.replace('.cookiedb', '') for f in db_files]
    return db_files
