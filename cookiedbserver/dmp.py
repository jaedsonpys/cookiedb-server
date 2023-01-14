# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# DMP - Database Manipulation Protocol
# 
# Protocol Request Structure:
# ACTION PATH:<DATABASE NAME> (required if requested "action" is GET, ADD, DEL, or UPD)
# <data (required if requested "action" is GET, ADD, DEL, or UPD)>
# 
# Protocol Response Structure:
# STATUS MESSAGE
# <data (required if requested "action" is GET, ADD, DEL, or UPD)>

import struct


class DMP:
    @staticmethod
    def parse_request(message: bytes) -> dict:
        request = {}

        action_field = message[:3]
        action = struct.unpack(f'3s', action_field)
        action = action[0].decode()

        remaining_fields = message[3:]
        fields = struct.unpack(f'{len(remaining_fields)}s', remaining_fields)

        if action in ('GET', 'ADD', 'UPD', 'DEL'):
            path, database = fields[0].split(b':')
            request['database'] = database.decode()
        elif action in ('CDB', 'LDB', 'DDB', 'ODB'):
            path = fields[0]

        request['path'] = path.decode()
        request['action'] = action

        return request
