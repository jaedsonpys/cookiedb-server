
from flask import Flask
from flask_cors import CORS

from blueprints.users import users

import config

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(users)

if __name__ == '__main__':
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
