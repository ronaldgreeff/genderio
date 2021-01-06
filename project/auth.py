from flask import (Blueprint, render_template, redirect, url_for, request,
    flash)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/signin')
def signin():
    return render_template("signin.html")

@auth.route('/signin', methods=['POST'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.signin'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')

    if password != repeat_password:
        flash("Passwords don't match.")
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists.")
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signin'))


@auth.route('/logout')
def logout():
    return 'Logout'
