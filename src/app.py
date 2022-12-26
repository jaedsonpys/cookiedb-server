
from flask import Flask
from flask_cors import CORS

from blueprints.users import users
from blueprints.database import database

import config

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(users)
app.register_blueprint(database, url_prefix='/database')

if __name__ == '__main__':
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
