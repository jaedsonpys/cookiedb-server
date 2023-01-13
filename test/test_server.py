import os
import shutil

import bupytest

HOST = '127.0.0.1'
USER_PW = '12345678'


class TestServer(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self._database = 'Market'
        self._temp_database = 'TempDatabase'

        self._database_data = {
            'banana': {
                'price': 1.50,
                'inStock': True
            },
            'cookie': {
                'price': 2.75,
                'inStock': False
            }
        }
        

if __name__ == '__main__':
    bupytest.this()
