from datetime import datetime, timedelta

import bcrypt
import utoken
from flask import Blueprint, jsonify
from flask import request

from config import users_db
from config import UTOKEN_SECRET_KEY

users = Blueprint('users', __name__)


def _users_exists(email: str) -> bool:
    user = users_db.get(f'users/{email}')
    return bool(user)


@users.route('/register', methods=['POST'])
def register():
    data: dict = request.json

    if not data:
        response = jsonify(status='error', message='no_data_found'), 400
    else:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            response = jsonify(status='error', message='email_and_password_required'), 400
        elif _users_exists(email):
            response = jsonify(status='error', message='email_already_used'), 409
        else:
            pw_salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode(), pw_salt)

            users_db.add(f'users/{email}', {
                'username': username,
                'email': email,
                'password': hashed_pw.decode()
            })

            exp_time = datetime.now() + timedelta(minutes=10)
            token = utoken.encode({'email': email, 'max-time': exp_time}, UTOKEN_SECRET_KEY)
            response = jsonify(status='success', token=token), 201

    return response


@users.route('/login', methods=['POST'])
def login():
    data: dict = request.json

    if not data:
        response = jsonify(status='error', message='no_data_found'), 400
    else:
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            response = jsonify(status='error', message='email_and_password_required'), 400
        elif not _users_exists(email):
            response = jsonify(status='error', message='email_or_password_invalid'), 401
        else:
            # confirm user password
            hashed_pw = users_db.get(f'users/{email}/password')
            hashed_pw = hashed_pw.encode()

            if bcrypt.checkpw(password.encode(), hashed_pw):
                exp_time = datetime.now() + timedelta(minutes=10)
                token = utoken.encode({'email': email, 'max-time': exp_time}, UTOKEN_SECRET_KEY)
                response = jsonify(status='success', token=token), 201
            else:
                response = jsonify(status='error', message='email_or_password_invalid'), 401

    return response
