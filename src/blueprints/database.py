import os
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


def _get_user_database(email: str) -> CookieDB:
    user_password = users_db.get(f'users/{email}/password')
    db = CookieDB(key=user_password, database_local=DATABASES_PATH)
    return db


@database.route('/database', methods=['GET', 'POST', 'DELETE'])
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
                new_db_id = generate_id()
                new_db = _get_user_database(user_email)
                new_db.create_database(new_db_id)

                # register database ID in user databases
                users_db.add(f'users/{user_email}/databases/{database_name}', new_db_id)
                response = jsonify(status='success', message='database_created'), 201
    elif request.method == 'DELETE':
        data = request.json

        if not data:
            response = jsonify(status='error', message='no_data_found'), 400
        else:
            user_email = payload['email']
            database_name = data.get('databaseName')
            
            if not database_name:
                response = jsonify(status='error', message='database_name_required'), 400
            elif not _database_exists(user_email, database_name):
                response = jsonify(status='error', message='database_not_exists'), 404
            else:
                user_database_path = f'users/{user_email}/databases/{database_name}'
                database_id = users_db.get(f'users/{user_email}/databases/{database_name}')
                
                cookiedb_file = os.path.join(DATABASES_PATH, f'{database_id}.cookiedb')
                users_db.delete(user_database_path)

                if os.path.isfile(cookiedb_file):
                    os.remove(cookiedb_file)

                response = jsonify(status='success', message='database_deleted'), 200
    elif request.method == 'GET':
        user_email = payload['email']
        databases = users_db.get(f'users/{user_email}/databases')
        response = jsonify(status='success', databases=list(databases.keys())), 200

    return response


@database.route('/database/<database_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@required_auth
def use_db(payload, database_name):
    if request.method == 'GET':
        data: dict = request.json

        if not data:
            response = jsonify(status='error', message='no_data_found'), 400
        else:
            user_email = payload['email']
            path = data.get('path')

            if not path:
                response = jsonify(status='error', message='path_required'), 400
            elif not _database_exists(user_email, database_name):
                response = jsonify(status='error', message='database_not_exists'), 404
            else:
                db_id = users_db.get(f'users/{user_email}/databases/{database_name}')
                db = _get_user_database(user_email)
                db.open(db_id)
                result = db.get(path)

                response = jsonify(status='success', result=result), 200
    elif request.method == 'POST':
        data: dict = request.json

        if not data:
            response = jsonify(status='error', message='no_data_found'), 400
        else:
            user_email = payload['email']
            path = data.get('path')
            value = data.get('value')

            if not all([path, value]):
                response = jsonify(status='error', message='path_and_item_required'), 400
            elif not _database_exists(user_email, database_name):
                response = jsonify(status='error', message='database_not_exists'), 404
            else:
                db = _get_user_database(user_email)
                db_id = users_db.get(f'users/{user_email}/databases/{database_name}')
                db.open(db_id)
                db.add(path, value)

                response = jsonify(status='success', message='item_added'), 201

    return response
