import os
import hashlib
import random
from pathlib import Path

HOME_USER = Path.home()
COOKIEDB_PATH = os.path.join(HOME_USER, '.cookiedbserver')
PASSWORD_PATH = os.path.join(COOKIEDB_PATH, 'password')


def check_config() -> None:
    return os.path.isdir(COOKIEDB_PATH)


def configure(password: str) -> None:
    salt = random.randint(0, 10)
    pw_with_salt = (password + str(salt)).encode()
    hashed_pw = hashlib.sha256(pw_with_salt)

    with open(PASSWORD_PATH, 'w') as file:
        file.write(hashed_pw)
