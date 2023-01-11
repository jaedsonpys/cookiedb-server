import json
import socket
import threading

from . import exceptions


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


class Server:
    def __init__(self, host: str = '127.0.0.1') -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._address = (host, 2808)
        self._socket.bind(self._address)
        self._listen(5)

    def _run(self) -> None:
        while True:
            client, addr = self._socket.accept()
            data = client.recv(1024)

    def run(self) -> None:
        print(f'Server started at {self._address[0]}:{self._address[1]}')

        server_th = threading.Thread(target=self._run)
        server_th.start()
