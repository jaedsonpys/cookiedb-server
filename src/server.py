import socket


class Server:
    def __init__(self, host: str = '127.0.0.1') -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, 2808))
        self._listen(5)

    def _run(self) -> None:
        while True:
            client, addr = self._socket.accept()
            data = client.recv(1024)
