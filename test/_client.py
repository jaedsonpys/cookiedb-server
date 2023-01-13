import socket


class Client:
    def __init__(self, host: str) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
