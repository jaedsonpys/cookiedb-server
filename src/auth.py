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

    @staticmethod
    def _get_connection_id(address: tuple) -> str:
        address_str = f'{address[0]}:{address[1]}'.encode()
        connection_id = hashlib.md5(address_str).hexdigest()
        return connection_id

    def login(self, address: tuple, password: str) -> bool:
        if self._check_password(password):
            connection_id = self._get_connection_id(address)
            self._logged_users.append(connection_id)
            return connection_id
        else:
            return False

    def logout(self, connection_id: str) -> bool:
        try:
            self._logged_users.remove(connection_id)
        except ValueError:
            return False
        else:
            return True
