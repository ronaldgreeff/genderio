from flask import (Blueprint, render_template, redirect, url_for, request,
    flash)
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from ..models import User
from .. import db
from ..email import send_email
from .forms import SigninForm, SignupForm
from .tokens import generate_confirmation_token, confirm_token
from datetime import datetime as dt
from . import auth
# auth = Blueprint('auth', __name__)


# TODO: forgot password

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
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    return render_template('unconfirmed.html')


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
        'signin.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
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


@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email_confirm.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
