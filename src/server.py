import socket
import threading


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
