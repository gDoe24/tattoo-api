import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Artist, Client, Appointment


# Primary handler of the application
# Contains Endpoints, CORS, Errors
def create_app(test_config=None):

    # create and configure the app, database, and CORS headers
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return "Hello Motto"

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
