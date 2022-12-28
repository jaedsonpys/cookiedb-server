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

        # wait server start
        print('Start the CookieDB Server in \033[1msrc/app.py\033[m')
        while True:
            try:
                requests.get(URL)
            except requests.exceptions.ConnectionError:
                continue
            else:
                break

    def test_register_user(self):
        req = requests.post(URL + '/register', json={
            'username': USER_NAME,
            'email': USER_EMAIL,
            'password': USER_PW
        })

        # expected 201 (Created)
        self.assert_expected(req.status_code, 201)

        response = req.json()

        self.assert_true(response['token'])
        self.assert_expected(response['status'], 'success')

        self._token = response['token']


if __name__ == '__main__':
    bupytest.this()
