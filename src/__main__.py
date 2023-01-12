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
    else:
        print('\033[32mWelcome to CookieDB Server!\033[m')
        print('Set a password to access your database.')
        print('Connections will only be allowed if the password is correct.\n')
        
        try:
            password = getpass.getpass('[?] Password: ')
            password = password.strip()

            confirm_pw = getpass.getpass('[?] Confirm the password: ')
            confirm_pw = confirm_pw.strip()

            while password != confirm_pw:
                confirm_pw = getpass.getpass('[?] Confirm the password (\033[31mTry Again\033[m): ')
                confirm_pw = confirm_pw.strip()
        except KeyboardInterrupt:
            print()
            return 0

        config.configure(password)
        print('\n\u2705 All right! Now you can run the server smoothly.')
