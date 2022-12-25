
from flask import Flask
from flask_cors import CORS
from cookiedb import CookieDB

import config

app = Flask(__name__)
cors = CORS(app)

if __name__ == '__main__':
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.SERVER_DEBUG
    )
