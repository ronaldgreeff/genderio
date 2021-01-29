from itsdangerous import URLSafeTimedSerializer
from flask import Flask, current_app
from project.config import Config


app = Flask(__name__)
app.config.from_object(Config)
# app = current_app._get_current_object()
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def generate_confirmation_token(email):
    """"""
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_email_token(token, expiration=3600):
    """ 1 hour window """
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration,
        )
        return email

    except:
        return False
