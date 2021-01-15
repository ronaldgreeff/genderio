from itsdangerous import URLSafeTimedSerializer
from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def generate_confirmation_token(email):
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration,
        )
    except:
        return False
    return email
