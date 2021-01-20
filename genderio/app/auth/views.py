from flask import (Blueprint, render_template, redirect, url_for, request,
    flash)
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from ..models import User
from .. import db
from ..email import send_email
from .forms import SigninForm, SignupForm, EmailForm, PasswordForm
from .tokens import generate_confirmation_token, confirm_email_token
from datetime import datetime as dt
from . import auth


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
                created_on=dt.now(),
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)

            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('email_confirm.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)

            print(confirm_url)

            flash('A confirmation has been sent via email.', 'success')

            return redirect(url_for('main.dashboard'))

        flash('A user already exists with that email address.', 'warning')

    return render_template('signup.html', form=form,)


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

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard', user_id= user.id))
        flash('Invalid username/password combination', 'danger')
        return redirect(url_for('auth.signin'))

    return render_template('signin.html', form=form,)


@auth.route('/confirm/<token>')
def confirm_email(token):

    try:
        email = confirm_email_token(token)
    except:
        flash('The confirmation link in invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Account already confirmed. Please Login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = dt.now()
        db.session.add(user)
        db.session.commit()

        login_user(user)

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


@auth.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        token = generate_confirmation_token(user.email)
        reset_url = url_for('auth.confirm_reset', token=token, _external=True)
        html = ('email_reset_password.html', reset)
        subject = "Reset your password"
        send_email(user.email, subject, html)

        print(reset_url)

        flash("A password reset email has been sent.", "success")
        return redirect(url_for('auth.signin'))

    return render_template('reset_request.html', form=form)

@auth.route('/reset/<token>', methods=["GET", "POST"])
def confirm_reset(token):
    try:
        email = confirm_email_token(token)
    except:
        flash("The confirmation link in invalid or has expired. Please try again.", "danger")
        return redirect(url_for('auth.reset'))

    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Password successfully changed.", "success")
        return redirect(url_for('auth.signin'))

    return render_template('reset_envoke.html', form=form, token=token)
