import os

import itchat

from .auth import auth_bp
from .wechat import wechat_bp
from .database import db
from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'development key'

    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(wechat_bp)

    return app