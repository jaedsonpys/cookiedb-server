# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

import json
import socket
import threading

from . import exceptions
from .auth import Auth
from .database import DBHandle


def parse(message: bytes) -> dict:
    result = {}

    message = message.decode()
    lines = message.split('\n')

    if len(lines) == 2:
        header, data = lines
        # parse data
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise exceptions.InvalidDataError('Invalid JSON data')
    else:
        header = lines[0]
        data = None

    try:
        # parse header
        action, path = header.split(' ')
    except ValueError:
        raise exceptions.InvalidMessageError('Invalid header error')

    result['data'] = data
    result['path'] = path
    result['action'] = action

    return result


def make_response(response: dict) -> bytes:
    status = response['status'].upper()
    message = response['message'].upper()

    msg = f'{status} {message}'

    if response.get('data'):
        json_data = json.dumps(response['data'])
        msg += f'\n{json_data}'

    return msg.encode()


class Server:
    def __init__(self, host: str = '127.0.0.1') -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._address = (host, 2808)
        self._socket.bind(self._address)
        self._socket.listen(5)

        self._auth = Auth()

    def _run(self) -> None:
        while True:
            client, addr = self._socket.accept()
            password = client.recv(1024).decode()
            conn_id = self._auth.login(addr, password)

            if conn_id:
                response = make_response({'status': 'success', 'message': 'login_successfully'})
                client.send(response)

                client_db = DBHandle()

                while True:
                    message = client.recv(5024)

                    if not message:
                        self._auth.logout(conn_id)
                        break

                    request = parse(message)
                    response = client_db.analyze_request(request)
                    client.send(make_response(response))
            else:
                response = make_response({'status': 'error', 'message': 'invalid_password'})
                client.send(response)
                client.close()

    def run(self) -> None:
        server_th = threading.Thread(target=self._run)
        server_th.setDaemon(True)
        server_th.start()

    def stop(self) -> None:
        self._socket.close()
