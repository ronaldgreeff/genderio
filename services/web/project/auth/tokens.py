import os
from itsdangerous import URLSafeTimedSerializer, BadData, BadSignature
from flask import Flask
from project.config import Config


serializer = URLSafeTimedSerializer(f"{os.getenv('SECRET_KEY')}")


def generate_confirmation_token(email):
    """Generate confirmation token using user's email address"""
    # return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    return serializer.dumps(email, salt=f"{os.getenv('SECURITY_PASSWORD_SALT')}")


def confirm_email_token(token, expiration=3600):
    """Confirm tokenized email within 1 hour"""
    try:
        email = serializer.loads(
            token,
            # salt=app.config['SECURITY_PASSWORD_SALT'],
            salt=f"{os.getenv('SECURITY_PASSWORD_SALT')}",
            max_age=expiration,
        )
        return email

    except (BadData, BadSignature):
        return False
