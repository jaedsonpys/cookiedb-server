import json
import socket
import threading

from . import exceptions
from .auth import Auth


def parse(message: bytes) -> None:
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
        method, path = header.split(' ')
    except ValueError:
        raise exceptions.InvalidMessageError('Invalid header error')

    result['data'] = data
    result['path'] = path
    result['method'] = method


def make_response(response: dict) -> bytes:
    status = response['status'].upper()
    message = response['message'].upper()
    data = response['data']

    msg = f'{status} {message}'

    if data:
        msg += f'\n{data}'

    return msg.encode()


class Server:
    def __init__(self, host: str = '127.0.0.1') -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._address = (host, 2808)
        self._socket.bind(self._address)
        self._listen(5)

        self._auth = Auth()

    def _run(self) -> None:
        while True:
            client, addr = self._socket.accept()
            password = client.recv(1024).decode()

            if self._auth.login(addr, password):
                response = make_response({'status': 'success', 'message': 'login_successfully'})
                client.send(response)

    def run(self) -> None:
        print(f'Server started at {self._address[0]}:{self._address[1]}')

        server_th = threading.Thread(target=self._run)
        server_th.start()
