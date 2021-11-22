import os
import secrets

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = secrets.token_hex()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        if 'username' in session:
            return f"You are logged in as {session['username']}"
        return "Please login first"

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import weather
    app.register_blueprint(weather.bp)

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username