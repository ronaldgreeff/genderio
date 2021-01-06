from flask import Blueprint, render_template
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signin')
def login():
    return render_template("signin.html")

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return 'Logout'
