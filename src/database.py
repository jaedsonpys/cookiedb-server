import os
import cookiedb
from .config import DATABASES_PATH
from .config import PASSWORD_PATH

with open(PASSWORD_PATH, 'r') as file:
    DATABASE_KEY = file.read()


def list_databases() -> list:
    db_files = os.listdir(DATABASES_PATH)
    db_files = [f.replace('.cookiedb', '') for f in db_files]
    return db_files
