import getpass

from . import config
from . import server
from . import auth


def main():
    if config.check_config():
        try:
            password = getpass.getpass('[?] Password: ')
            password = password.strip()

            while not auth.Auth._check_password(password):
                password = getpass.getpass('[?] Password (\033[31mTry Again\033[m): ')
                password = password.strip()
        except KeyboardInterrupt:
            print()
            return 0

        sock = server.Server()
        sock.run()

        print('Server has running...')

        while 1:
            try:
                pass
            except KeyboardInterrupt:
                print('\nServer stopped.')
                sock.stop()
                return 0
