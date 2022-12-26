import dotenv
from cookiedb import CookieDB

env = dotenv.dotenv_values('.env')

# enviroment variables
SERVER_DATABASE_KEY = env.get('SERVER_DATABASE_KEY')
UTOKEN_SECRET_KEY = env.get('UTOKEN_SECRET_KEY')
FLASK_SECRET_KEY = env.get('FLASK_SECRET_KEY')
DATABASES_PATH = env.get('DATABASES_PATH')

SERVER_HOST = env.get('SERVER_HOST', '127.0.0.1')
SERVER_PORT = env.get('SERVER_PORT', 5500)
SERVER_DEBUG = bool(env.get('SERVER_DEBUG', False))

SERVER_CONFIG_DB = 'cookiedb-server'
USERS_DB = 'cookiedb-users'

# users database
users_db = CookieDB(
    key=SERVER_DATABASE_KEY,
    database_local='./'
)

users_db.create_database(USERS_DB, if_not_exists=True)
users_db.open(USERS_DB)