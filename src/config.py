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

import os

import dotenv
from cookiedb import CookieDB

env = dotenv.dotenv_values('.env')

# enviroment variables
SERVER_DATABASE_KEY = env.get('SERVER_DATABASE_KEY')
UTOKEN_SECRET_KEY = env.get('UTOKEN_SECRET_KEY')
DATABASES_PATH = env.get('DATABASES_PATH')

SERVER_HOST = env.get('SERVER_HOST', '127.0.0.1')
SERVER_PORT = env.get('SERVER_PORT', 5500)
SERVER_DEBUG = bool(env.get('SERVER_DEBUG', False))

SERVER_CONFIG_DB = 'cookiedb-server'
USERS_DB = 'cookiedb-users'

if not all([SERVER_DATABASE_KEY, UTOKEN_SECRET_KEY]):
    import sys
    print('Please set SERVER_DATABASE_KEY and FLASK_SECRET_KEY '
          'enviroments variables!')

    sys.exit(1)

# users database
users_db = CookieDB(
    key=SERVER_DATABASE_KEY,
    database_local='./'
)

users_db.create_database(USERS_DB, if_not_exists=True)
users_db.open(USERS_DB)

if not os.path.isdir('./database'):
    os.mkdir('./database')
