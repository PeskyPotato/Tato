from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import User
from . import db

import re

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check login details and try again.', "error")
        return redirect(url_for("auth.login"))

    # creates session
    login_user(user, remember=remember)

    return redirect(url_for("profile.profile_route"))

def signup_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config["SIGNUP"]:
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function


@auth.route("/signup")
@signup_check
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
@signup_check
def signup_post():
    username = request.form.get("username")
    name = request.form.get("name")
    password = request.form.get("password")

    if not (password_check(password).get("password_ok", False)):
        flash("Your password is not strong enough, make sure it meets the following requirements:", "error")
        flash("8 or more characters", "error")
        flash("1 or more lowercase letters", "error")
        flash("1 or more uppercase letters", "error")
        flash("1 or more special characters", "error")
        flash("1 or more digits", "error")
        return redirect(url_for("auth.signup"))

    if not username.isalnum():
        flash("Inavlid uesrname.", "error")
        return redirect(url_for("auth.signup"))

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists.', "error")
        return redirect(url_for("auth.signup"))

    new_user = User(username=username, name=name,
                    password=generate_password_hash(password, method="sha256"))

    db.session.add(new_user)
    db.session.commit()

    flash("Successfully signed up!", "success")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


def password_check(password):
    """
    Source: https://stackoverflow.com/a/32542964/6340707
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
