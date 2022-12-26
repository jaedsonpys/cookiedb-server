import secrets

import cookiedb
from flask import Blueprint

from config import users_db

database = Blueprint('database', __name__)


def generate_id() -> str:
    db_id = secrets.token_hex(16)
    return db_id
