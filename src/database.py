import os
from typing import Any

import cookiedb
from .config import DATABASES_PATH
from .config import PASSWORD_PATH


class DBHandle:
    def __init__(self) -> None:
        with open(PASSWORD_PATH, 'r') as file:
            key = file.read()

        self._db = cookiedb.CookieDB(key, DATABASES_PATH)

    @staticmethod
    def _list_databases() -> list:
        db_files = os.listdir(DATABASES_PATH)
        db_files = [f.replace('.cookiedb', '') for f in db_files]
        return db_files

    @staticmethod
    def _delete_database(name: str) -> dict:
        db_file = os.path.join(DATABASES_PATH, f'{name}.cookiedb')

        if os.path.isfile(db_file):
            os.remove(db_file)

        return dict(status='success', message='database_deleted')

    def _create_database(self, name: str) -> dict:
        try:
            self._db.create_database(name, if_not_exists=name.endswith('?'))
        except cookiedb.exceptions.DatabaseExistsError:
            response = dict(status='error', message='database_exists')
        else:
            response = dict(status='success', message='database_created')

        return response

    def _add_item(self, database: str, path: str, item: Any) -> dict:
        self._db.open(database)
        self._db.add(path, item)
        return dict(status='success', message='item_added')

    def analyze_request(self, request: dict) -> dict:
        action = request['action']
        path = request['path']

        # Server Operations: Create database (CDB),
        # delete database (DDB), open database (ODB)
        # and list database (LDB).
        if action == 'CDB':
            response = self._create_database(path)
        elif action == 'DDB':
            response = self._delete_database(path)
        elif action == 'LDB':
            response = self._list_databases()

        return response
