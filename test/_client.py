import json
import struct
import socket

from typing import Any

import cookiedb


class NoneData:
    pass


def parse(response: bytes) -> dict:
    parsed_response = {}
    split_response = response.split(b'\n')

    header = split_response[0]
    status, = struct.unpack(f'4s', header[:4])
    message, = struct.unpack(f'{len(header[4:])}s', header[4:])

    parsed_response['status'] = status.decode()
    parsed_response['message'] = message.decode()

    if len(split_response) == 2:
        data = split_response[1]
        datatype, = struct.unpack('4s', data[:4])
        rdata = data[4:]

        if datatype == b'json':
            _data = json.loads(rdata)
        elif datatype == b'intg':
            _data = int.from_bytes(rdata, byteorder='big')
        elif datatype == b'flot':
            _data, = struct.unpack('f', rdata)
        elif datatype == b'stri':
            _data = rdata.decode()
        elif datatype == b'bool':
            _data, = struct.unpack('?', rdata)
        elif datatype == b'none':
            _data = None

        parsed_response['data'] = _data

    return parsed_response


def make_request(request: dict) -> bytes:
    action = request['action']
    path = request['path']

    packed = struct.pack(f'3s {len(path)}s', action.encode(), path.encode())
    data = request.get('data', NoneData)

    if data is not NoneData:
        if isinstance(data, (list, dict, tuple)):
            json_data = json.dumps(data, separators=(',', ':'))
            datatype = struct.pack('4s', b'json')
            _encoded_data = json_data.encode()
        elif isinstance(data, str):
            datatype = struct.pack('4s', b'stri')
            _encoded_data = data.encode()
        elif isinstance(data, bool):
            datatype = struct.pack('4s', b'bool')
            _encoded_data = struct.pack('?', data)
        elif isinstance(data, int):
            datatype = struct.pack('4s', b'intg')
            _encoded_data = data.to_bytes(2, byteorder='big')
        elif isinstance(data, float):
            datatype = struct.pack('4s', b'flot')
            _encoded_data = struct.pack('f', data)
        elif data is None:
            datatype = struct.pack('4s', b'none')
            _encoded_data = b'None'

        packed += b'\n'
        packed += datatype + _encoded_data

    return packed


class Client:
    def __init__(self) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._opened_database = None

    def connect(self, host: str, password: str) -> None:
        self._client.connect((host, 2808))
        self._client.send(password.encode())

        response = self._client.recv(1024)
        response = parse(response)

        if response['status'] != 'OKAY':
            raise ConnectionError('Invalid password to connect')

    def _request(self, request: dict) -> dict:
        request = make_request(request)
        self._client.send(request)
        response = self._client.recv(1024)
        response = parse(response)

        return response

    def list_databases(self) -> list:
        databases = self._request({'action': 'LDB', 'path': 'None'})
        return databases['data']

    def open(self, database: str) -> None:
        databases = self.list_databases()
        if database in databases:
            self._opened_database = database
        else:
            raise cookiedb.exceptions.DatabaseNotFoundError('Database not exists')

    def create_database(self, database: str, if_not_exists: bool = False) -> None:
        response = self._request({'action': 'CDB', 'path': database})

        if response['message'] == 'DATABASE_EXISTS' and not if_not_exists:
            raise cookiedb.exceptions.DatabaseExistsError('Database already exists')

    def delete_database(self, database: str) -> list:
        self._request({'action': 'DDB', 'path': database})

    def add(self, path: str, item: Any) -> None:
        _path = f'{path}:{self._opened_database}'
        self._request({'action': 'ADD', 'path': _path, 'data': item})

    def update(self, path: str, item: Any) -> None:
        _path = f'{path}:{self._opened_database}'
        response = self._request({'action': 'UPD', 'path': _path, 'data': item})

        if response['message'] == 'item_not_exists_error':
            raise cookiedb.exceptions.ItemNotExistsError(f'Item "{item}" not exists')

    def get(self, path: str) -> Any:
        _path = f'{path}:{self._opened_database}'
        response = self._request({'action': 'GET', 'path': _path})
        return response['data']

    def delete(self, path: str) -> Any:
        _path = f'{path}:{self._opened_database}'
        self._request({'action': 'DEL', 'path': _path})
