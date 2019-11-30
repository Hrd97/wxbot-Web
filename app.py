import os
import auth
from database import db
from flask import Flask,render_template
def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    @app.route("/")
    def hello():
        return render_template("auth/register.html")
       # return "Hello, World!"

    # register the database commands
    #from db import db

    db.init_app(app)

    # apply the blueprints to the app
    #from flaskr import auth, blog

    app.register_blueprint(auth.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #
    app.add_url_rule("/", endpoint="index")
    #app.add_url_rule("/", endpoint="auth")
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0")
