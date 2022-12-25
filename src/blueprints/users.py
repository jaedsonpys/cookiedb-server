import hashlib
import random

import bcrypt
from flask import Blueprint, jsonify
from flask import request

from config import users_db

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
            return jsonify(status='error', message='email_and_password_required'), 400
        else:
            uuid_salt = str(random.randint(10000000, 99999999))
            pre_uuid = username + email + uuid_salt
            uuid = hashlib.md5(pre_uuid)

            pw_salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode(), pw_salt)

            users_db.add(f'users/{email}', {
                'uuid': uuid,
                'username': username,
                'email': email,
                'password': hashed_pw.decode()
            })
