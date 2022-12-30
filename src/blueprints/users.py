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

from datetime import datetime, timedelta

import bcrypt
import utoken
from flask import Blueprint, jsonify
from flask import request

from auth import _users_exists
from config import users_db
from config import UTOKEN_SECRET_KEY

users = Blueprint('users', __name__)


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
            response = jsonify(status='error', message='username_email_and_password_required'), 400
        elif _users_exists(email):
            response = jsonify(status='error', message='email_already_used'), 409
        else:
            pw_salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode(), pw_salt)

            users_db.add(f'users/{email}', {
                'username': username,
                'email': email,
                'password': hashed_pw.decode(),
                'databases': {}
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
