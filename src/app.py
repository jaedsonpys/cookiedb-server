
from flask import Flask
from flask_cors import CORS
from cookiedb import CookieDB

import config

app = Flask(__name__)
cors = CORS(app)

users_db = CookieDB(
    key=config.SERVER_DATABASE_KEY,
    database_local='./'
)

users_db.create_database(config.USERS_DB, if_not_exists=True)
users_db.open(config.USERS_DB)

if __name__ == '__main__':
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
