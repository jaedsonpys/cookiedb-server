# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

import socket
import threading

from .dmp import DMP
from .auth import Auth
from .database import DBHandle


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
                response = DMP.parse_response('OKAY', 'login_successfully')
                client.send(response)

                client_db = DBHandle()

                while True:
                    message = client.recv(5024)

                    if not message:
                        self._auth.logout(conn_id)
                        break

                    request = DMP.parse_request(message)
                    response = client_db.analyze_request(request)

                    client_response = DMP.parse_response(
                        status=response['status'],
                        message=response['message'],
                        data=response.get('data')
                    )

                    client.send(client_response)
            else:
                response = DMP.parse_response('FAIL', 'invalid_password')
                client.send(response)
                client.close()

    def run(self) -> None:
        server_th = threading.Thread(target=self._run)
        server_th.setDaemon(True)
        server_th.start()

    def stop(self) -> None:
        self._socket.close()
