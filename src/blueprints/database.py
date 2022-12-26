import secrets

from cookiedb import CookieDB
from flask import Blueprint, jsonify
from flask import request

from config import users_db
from config import DATABASES_PATH
from auth import required_auth

database = Blueprint('database', __name__)


def generate_id() -> str:
    db_id = secrets.token_hex(16)
    return db_id


def _database_exists(user_email: str, database_name: str) -> bool:
    databases = users_db.get(f'users/{user_email}/databases')
    return database_name in databases


@database.route('/', methods=['GET', 'POST', 'DELETE'])
@required_auth
def db_handle(payload):
    if request.method == 'POST':
        data = request.json

        if not data:
            response = jsonify(status='error', message='no_data_found'), 400
        else:
            user_email = payload['email']
            database_name = data.get('databaseName')
            
            if not database_name:
                response = jsonify(status='error', message='database_name_required'), 400
            elif _database_exists(user_email, database_name):
                response = jsonify(status='error', message='database_already_exists'), 409
            else:
                user_password = users_db.get(f'users/{user_email}/password')
                new_db_id = generate_id()

                new_db = CookieDB(key=user_password, database_local=DATABASES_PATH)
                new_db.create_database(new_db_id)

                # register database ID in user databases
                users_db.add(f'users/{user_email}/databases', {
                    database_name: new_db_id
                })

                response = jsonify(status='success', message='database_created'), 201

        return response
