from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    Regexp,
)


class SignupForm(FlaskForm):
    """User registration form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password requires a minimum of 6 characters.'),
            Regexp(r"\d", message='Password should contain at least one digit.'),
            Regexp(r"[A-Z]", message='Password should contain at least one uppercase letter.'),
            Regexp(r"[a-z]", message='Password should contain at least one lowercase letter.'),
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class SigninForm(FlaskForm):
    """User sign-in form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class EmailForm(FlaskForm):
    """Reset password for email"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')


class PasswordForm(FlaskForm):
    """Choose new password"""
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Confirm')
