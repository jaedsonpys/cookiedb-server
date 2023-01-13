import socket
import json

from typing import Any

import cookiedb


def parse(self, response: bytes) -> dict:
    parsed_response = {}

    response = response.decode()
    lines = response.split('\n')

    header = lines[0]
    status, message = header.split(' ')
    response['status'] = status
    response['message'] = message
    
    if len(lines) == 2:
        data = lines[1]
        json_data = json.loads(data)
        response['data'] = json_data

    return parsed_response


def make_request(self, request: dict) -> bytes:
    action = request['action'].upper()
    path = request['path'].upper()

    msg = f'{action} {path}'

    if request.get('data'):
        json_data = json.dumps(request['data'])
        msg += f'\n{json_data}'

    return msg.encode()


class Client:
    def __init__(self) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._opened_database = None

    def connect(self, host: str, password: str) -> None:
        self._client.connect((host, 2808))
        self._client.send(password.encode())

        response = self._client.recv(1024)
        response = parse(response)

        if response['status'] != 'SUCCESS':
            raise ConnectionError('Invalid password to connect')

    def _request(self, request: dict) -> dict:
        request = make_request(request)
        self._client.send(request)
        response = self._client.recv(1024)
        response = parse(response)

        return response

    def list_databases(self) -> list:
        databases = self._request({'action': 'LDB', 'path': None})
        return databases

    def open(self, database: str) -> None:
        databases = self.list_databases()
        if database in databases:
            self._opened_database = database
        else:
            raise cookiedb.exceptions.DatabaseNotFoundError('Database not exists')

    def create_database(self, database: str, if_not_exists: bool = False) -> None:
        databases = self.list_databases()

        if database in databases and not if_not_exists:
            raise cookiedb.exceptions.DatabaseExistsError('Database already exists')
        else:
            self._request({'action': 'CDB', 'path': database})

    def add(self, path: str, item: Any) -> None:
        self._request({'action': 'ADD', 'path': path, 'data': item})

    def get(self, path: str) -> Any:
        response = self._request({'action': 'GET', 'path': path})
        return response['data']

    def delete(self, path: str) -> Any:
        self._request({'action': 'DEL', 'path': path})
