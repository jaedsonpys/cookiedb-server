import dotenv

env = dotenv.dotenv_values('.env')

# enviroment variables
SERVER_DATABASE_KEY = env.get('SERVER_DATABASE_KEY')
FLASK_SECRET_KEY = env.get('FLASK_SECRET_KEY')
UTOKEN_SECRET_KEY = env.get('UTOKEN_SECRET_KEY')

SERVER_CONFIG_DB = 'cookiedb-server'
USERS_DB = 'cookiedb-users'
