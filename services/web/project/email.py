import os
from flask import Flask, current_app
from flask_mail import Message, Mail
from project.config import Config
from . import mail


def send_email(to, subject, template):
    """General send mail function. Takes 'to', 'subject' and 'template' """
    # app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=f"{os.getenv("MAIL_DEFAULT_SENDER")}"
    )
    mail.send(msg)
