from flask import (Blueprint, render_template, redirect, url_for, request,
    flash)
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from .models import User
from . import db
from .emails import send_email
from .auth_forms import SigninForm, SignupForm
from .auth_token import generate_confirmation_token, confirm_token
from datetime import datetime as dt


auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SigninForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard', user_id= user.id))
        flash('Invalid username/password combination')
        return redirect(url_for('auth.signin'))

    return render_template(
        'signin.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    return render_template('unconfirmed.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('email_confirm.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)

            flash('A confirmation has been sent via email.', 'success')

            return redirect(url_for('main.dashboard'))
            # return redirect(url_for('auth.unconfirmed'))

        flash('A user already exists with that email address.')

    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )

@auth.route('/confirm/<token>')
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        print('The confirmation link in invalid or has expired.')
        flash('The confirmation link in invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        print('Account already confirmed. Please Login.')
        flash('Account already confirmed. Please Login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = dt.now()
        db.session.add(user)
        db.session.commit()
        print('You have confirmed your account. Thanks!')
        flash('You have confirmed your account. Thanks!', 'success')
        login_user(user)  # Log in as newly created user
    return redirect(url_for('main.dashboard'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))








# @auth.route('/signin')
# def signin():
#     return render_template("signin.html")
#
# @auth.route('/signin', methods=['POST'])
# def signin_post():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False
#
#     user = User.query.filter_by(email=email).first()
#
#     # if not user or not check_password_hash(user.password, password):
#     #     flash("Please check your login details and try again.")
#     #     return redirect(url_for('auth.signin'))
#     # TODO:
#
#     login_user(user, remember=remember)
#     return redirect(url_for('main.index'))
#
#
# @auth.route('/signup')
# def signup():
#     return render_template("signup.html")
#
# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     repeat_password = request.form.get('repeat_password')
#
#     if password != repeat_password:
#         flash("Passwords don't match.")
#         return redirect(url_for('auth.signup'))
#
#     user = User.query.filter_by(email=email).first()
#     if user:
#         flash("Email address already exists.")
#         return redirect(url_for('auth.signup'))
#
#     # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
#     new_user = User(email=email, name=name)
#     new_user.set_password()
#
#     db.session.add(new_user)
#     db.session.commit()
#
#     return redirect(url_for('auth.signin'))
