import utoken

from flask import request
from flask import jsonify

from config import UTOKEN_SECRET_KEY


def required_auth(func):
    def wrapper(*args, **kwargs):
        authorization = request.headers.get('Authorization')
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
                utoken.decode(token, UTOKEN_SECRET_KEY)
            except utoken_exceptions:
                response = jsonify(status='error', message='invalid_auth_token'), 401
            else:
                response = func(*args, **kwargs)
        else:
            response = jsonify(status='error', message='bearer_auth_required'), 401

        return response

    return wrapper
