import os

from flask import Flask
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource


class FlaskFactory :
    def __init__(self, test_config = None):
        app = Flask(__name__)
        # create and configure the app
        app = Flask(__name__, instance_relative_config=True)
        CORS(app, supports_credentials=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the tests config if passed in
            app.config.from_mapping(test_config)

        # init db
        db.init_app(app)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # a simple page that says hello
        @app.route('/hello')
        def hello():
            return 'Hello, World!'

        self.app = app
        self.api = Api(self.app)
