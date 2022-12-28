import bupytest
import requests

URL = 'http://127.0.0.1:5500'
USER_NAME = 'ThisTest'
USER_EMAIL = 'test@cookiedb.com'
USER_PW = '12345678'


class TestAPI(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

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
