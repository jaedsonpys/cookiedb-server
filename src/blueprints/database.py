import cookiedb
from flask import Blueprint

from config import users_db

database = Blueprint('database', __name__)
