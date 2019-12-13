import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from models import Users
from .database import db
from .forms import LoginForm, RegisterForm



auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@auth_bp.before_app_request
def load_logged_in_user():
    """If a wechat id is stored in the session, load the wechat object from
    the database into ``g.wechat``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter(Users.id == user_id).first()

@auth_bp.route("/register", methods=("GET", "POST"))
def register():

    form = RegisterForm()
    if request.method == "POST":
        phoneNumber = request.form["phonenumber"]
        password = request.form["password"]
        error = None
        if not phoneNumber:
            error = "phoneNumber is required."
        elif not password:
            error = "Password is required."
        elif (
            # db.execute("SELECT id FROM wechat WHERE username = ?", (username,)).fetchone()
            # is not None
            Users.query.filter(Users.phonenum == phoneNumber).first() is not None
        ):
            error = "User {0} is already registered.".format(phoneNumber)

        if error is None:
            db.session.add(Users(phonenum=phoneNumber, password=generate_password_hash(password)))
            db.session.commit()
            return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered wechat by adding the wechat id to the session."""
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpenID="' + form.phonenumber.data + '", remember_me=' + form.password.data)
        # print('Login requested for OpenID="' + form.phonenumber.data + '", remember_me=' + form.password.data)
    #     return redirect('/index')
    # if request.method == "POST":
        phoneNumber = request.form["phonenumber"]
        password = request.form["password"]
        error = None
        # print(phoneNumber)
        # print(password)
        users = Users.query.filter(Users.phonenum == phoneNumber).first()
        if users is None:
            error = "Incorrect username."
        elif not check_password_hash(users.password, password):
            error = "Incorrect password."

        if error is None:
            # store the wechat id in a new session and return to the index
            session.clear()
            session["user_id"] = users.id
            #return render_template('wechat/index.html', alive=bot.alive, bot=bot)
            return redirect(url_for('wechat.index'))
            #return redirect(url_for('auth.userInterface', userid=users.id))
        flash(error)
    return render_template("auth/login.html",form= form)

@auth_bp.route("/user/<int:userid>")
def userInterface(userid):
    """Clear the current session, including the stored wechat id."""
    return render_template("auth/user.html", userid=userid)

@auth_bp.route("/logout")
def logout():
    """Clear the current session, including the stored wechat id."""
    session.clear()
    return "logout ok"
    #return redirect(url_for("index"))
