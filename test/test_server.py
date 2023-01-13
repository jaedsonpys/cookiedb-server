import os
import shutil

import bupytest

HOST = '127.0.0.1'
USER_PW = '12345678'


class TestServer(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self._token = None
        self._database_1 = 'TestDatabase'
        self._database_2 = 'Market'
        self._database_3 = 'TempDatabase'

        self._database_1_data = {
            'python': {
                'creator': 'Guido'
            },
            'javascript': {
                'creator': 'Brendan'
            }
        }

        self._database_2_data = {
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
