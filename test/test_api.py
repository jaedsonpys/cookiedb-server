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

        self._token = None
        self._database_1 = 'TestDatabase'
        self._database_2 = 'Market'

        if os.path.isdir('./database'):
            shutil.rmtree('./database', ignore_errors=True)

        if os.path.isfile('./cookiedb-users.cookiedb'):
            os.remove('./cookiedb-users.cookiedb')

        # Please run the test before run the server. 
        # wait server start
        print('Start the CookieDB Server in \033[1msrc/app.py\033[m')
        while True:
            try:
                requests.get(URL)
            except requests.exceptions.ConnectionError:
                continue
            else:
                break
        
    def _get_auth_header(self):
        return {'Authorization': f'Bearer {self._token}'}

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

    def test_register_same_user(self):
        req = requests.post(URL + '/register', json={
            'username': USER_NAME,
            'email': USER_EMAIL,
            'password': USER_PW
        })

        # expected 409 (Conflict)
        self.assert_expected(req.status_code, 409)
        response = req.json()

        self.assert_expected(response['status'], 'error')
        self.assert_expected(response['message'], 'email_already_used')

    def test_register_data_required_error(self):
        # removing email and password from register data
        req = requests.post(URL + '/register', json={
            'username': USER_NAME
        })

        # expected 400 (Bad Request)
        self.assert_expected(req.status_code, 400)
        response = req.json()

        self.assert_expected(response['status'], 'error')
        self.assert_expected(response['message'], 'username_email_and_password_required')

    def test_login_user(self):
        req = requests.post(URL + '/login', json={
            'email': USER_EMAIL,
            'password': USER_PW
        })

        # expected 201 (Created)
        self.assert_expected(req.status_code, 201)

        response = req.json()

        self.assert_true(response['token'])
        self.assert_expected(response['status'], 'success')
        self._token = response['token']

    def test_invalid_login_data(self):
        req = requests.post(URL + '/login', json={
            'email': USER_EMAIL,
            'password': 'invalid_password'
        })

        # expected 401 (Unauthorized)
        self.assert_expected(req.status_code, 401)

        response = req.json()

        self.assert_expected(response['status'], 'error')
        self.assert_expected(response['message'], 'email_or_password_invalid')

    def test_login_data_required_error(self):
        # removing email from login data
        req = requests.post(URL + '/login', json={
            'password': USER_NAME
        })

        # expected 400 (Bad Request)
        self.assert_expected(req.status_code, 400)
        response = req.json()

        self.assert_expected(response['status'], 'error')
        self.assert_expected(response['message'], 'email_and_password_required')

    def test_create_database(self):
        req = requests.post(
            url=(URL + '/database'),
            json={'databaseName': self._database_1},
            headers=self._get_auth_header()
        )

        # expected 201 (Created)
        self.assert_expected(req.status_code, 201)

        response = req.json()

        self.assert_expected(response['status'], 'success')
        self.assert_expected(response['message'], 'database_created')

    def test_create_other_database(self):
        req = requests.post(
            url=(URL + '/database'),
            json={'databaseName': self._database_2},
            headers=self._get_auth_header()
        )

        # expected 201 (Created)
        self.assert_expected(req.status_code, 201)

        response = req.json()

        self.assert_expected(response['status'], 'success')
        self.assert_expected(response['message'], 'database_created')

    def test_create_database_with_same_name(self):
        req = requests.post(
            url=(URL + '/database'),
            json={'databaseName': self._database_1},
            headers=self._get_auth_header()
        )

        # expected 409 (Conflict)
        self.assert_expected(req.status_code, 409)

        response = req.json()

        self.assert_expected(response['status'], 'error')
        self.assert_expected(response['message'], 'database_already_exists')

    def test_list_databases(self):
        req = requests.get(URL + '/database', headers=self._get_auth_header())
        self.assert_expected(req.status_code, 200)

        response = req.json()

        self.assert_expected(response['status'], 'success')
        self.assert_expected(response['result'], [self._database_1, self._database_2])


if __name__ == '__main__':
    bupytest.this()
