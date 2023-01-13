import os
import sys
import shutil
from pathlib import Path

import bupytest
import cookiedb

from _client import Client

sys.path.insert(0, './')

from src.server import Server
from src.config import configure

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

        home_dir = Path.home()
        server_dir = os.path.join(home_dir, '.cookiedbserver')

        if os.path.isdir(server_dir):
            shutil.rmtree(server_dir)

        # configure server
        configure(USER_PW)

        # run server
        server = Server()
        server.run()

        self.db = Client()
        self.db.connect('127.0.0.1', USER_PW)

    def test_create_database(self):
        self.db.create_database(self._database)
        self.db.create_database(self._temp_database)

        self.assert_expected(self.db.list_databases(), [self._database, self._temp_database])

    def test_create_same_database(self):
        try:
            self.db.create_database(self._database)
        except cookiedb.exceptions.DatabaseExistsError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Expected a DatabaseExistsError exception')

    def test_delete_database(self):
        self.db.delete_database(self._temp_database)

    def test_list_databases(self):
        databases = self.db.list_databases()
        self.assert_expected(databases, [self._database])


if __name__ == '__main__':
    bupytest.this()
