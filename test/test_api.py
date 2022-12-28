import os
import shutil

import bupytest
import requests

URL = 'http://127.0.0.1:5500'
USER_NAME = 'ThisTest'
USER_EMAIL = 'test@cookiedb.com'
USER_PW = '12345678'


class TestAPI(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        if os.path.isdir('./database'):
            shutil.rmtree('./database', ignore_errors=True)

        if os.path.isfile('./cookiedb-users.cookiedb'):
            os.remove('./cookiedb-users.cookiedb')


if __name__ == '__main__':
    bupytest.this()
