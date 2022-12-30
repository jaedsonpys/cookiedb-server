# CookieDB database server
# Copyright (C) 2023  Jaedson Silva

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from functools import wraps

import utoken

from flask import request
from flask import jsonify

from config import UTOKEN_SECRET_KEY
from config import users_db


def _users_exists(email: str) -> bool:
    user = users_db.get(f'users/{email}')
    return bool(user)


def required_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get('Authorization')

        if authorization:
            auth_info = authorization.split(' ')

            if len(auth_info) == 2 and auth_info[0] == 'Bearer':
                token = auth_info[1]
                utoken_exceptions = (
                    utoken.exceptions.ExpiredTokenError,
                    utoken.exceptions.InvalidKeyError,
                    utoken.exceptions.InvalidTokenError,
                    utoken.exceptions.InvalidContentTokenError
                )

                try:
                    payload = utoken.decode(token, UTOKEN_SECRET_KEY)
                except utoken_exceptions:
                    response = jsonify(status='error', message='new_token_required'), 401
                else:
                    response = func(payload, *args, **kwargs)
            else:
                response = jsonify(status='error', message='bearer_auth_required'), 401
        else:
            response = jsonify(status='error', message='bearer_auth_required'), 401

        return response

    return wrapper
