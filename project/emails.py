from flask import Flask
from flask_mail import Message, Mail
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
