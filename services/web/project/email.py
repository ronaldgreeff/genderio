import os
from flask import Flask, current_app
from flask_mail import Message, Mail
from project.config import Config
from . import mail
# app = Flask(__name__)
# app.config.from_object(Config)
# mail = Mail(app)


def send_email(to, subject, template):
    # app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.getenv("MAIL_DEFAULT_SENDER")  # app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
