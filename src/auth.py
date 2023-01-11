import hashlib

from .config import PASSWORD_PATH


class Auth:
    def __init__(self) -> None:
        self._logged_users = []

    @staticmethod
    def _check_password(password: str) -> bool:
        with open(PASSWORD_PATH, 'rb') as file:
            hashed_pw = file.read()

        for salt in range(0, 11):
            pw_and_salt = (password + str(salt)).encode()
            try_pw_hash = hashlib.sha256(pw_and_salt)

            if hashed_pw == try_pw_hash:
                # password match
                return True

        return False

    def login(self, address: tuple, password: str) -> bool:
        if self._check_password(password):
            address_str = ':'.join(address).encode()
            connection_id = hashlib.md5(address_str).hexdigest()
            self._logged_users.append(connection_id)
            return True
        else:
            return False
