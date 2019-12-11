import os
from . import auth, wechat
from .database import db
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'development key'


    db.init_app(app)


    app.register_blueprint(auth.bp)
    app.register_blueprint(wechat.bp)

    return app