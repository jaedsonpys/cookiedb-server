import os
import sys
import shutil

import bupytest

from _client import Client

sys.path.insert(0, './')

from src.server import Server

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

        server = Server()
        server.run()

        self.db = Client()
        self.db.connect('127.0.0.1', USER_PW)

    def test_create_database(self):
        self.db.create_database(self._database)
        self.db.create_database(self._temp_database)

        self.assert_expected(self.db.list_databases(), [self._database, self._temp_database])


if __name__ == '__main__':
    bupytest.this()
