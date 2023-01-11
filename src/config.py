import os
import hashlib
import random
from pathlib import Path

HOME_USER = Path.home()
COOKIEDB_PATH = os.path.join(HOME_USER, '.cookiedbserver')
PASSWORD_PATH = os.path.join(COOKIEDB_PATH, 'password')
DATABASES_PATH = os.path.join(COOKIEDB_PATH, 'databases')


def check_config() -> None:
    return all([
        os.path.isdir(COOKIEDB_PATH),
        os.path.isfile(PASSWORD_PATH),
        os.path.isdir(DATABASES_PATH)
    ])


def configure(password: str) -> None:
    os.mkdir(COOKIEDB_PATH)
    os.mkdir(DATABASES_PATH)

    salt = random.randint(0, 10)
    pw_with_salt = (password + str(salt)).encode()
    hashed_pw = hashlib.sha256(pw_with_salt).hexdigest()

    with open(PASSWORD_PATH, 'w') as file:
        file.write(hashed_pw)
