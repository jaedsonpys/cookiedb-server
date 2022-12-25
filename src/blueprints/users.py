import bcrypt
from flask import Blueprint, jsonify
from flask import request

from config import users_db

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
            return jsonify(status='error', message='email_and_password_required'), 400
        elif _users_exists(email):
            return jsonify(status='error', message='email_already_used'), 409
        else:
            pw_salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode(), pw_salt)

            users_db.add(f'users/{email}', {
                'username': username,
                'email': email,
                'password': hashed_pw.decode()
            })
