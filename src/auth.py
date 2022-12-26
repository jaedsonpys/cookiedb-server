import utoken

from flask import request
from flask import jsonify

from config import UTOKEN_SECRET_KEY
from config import users_db


def _users_exists(email: str) -> bool:
    user = users_db.get(f'users/{email}')
    return bool(user)


def required_auth(func):
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
