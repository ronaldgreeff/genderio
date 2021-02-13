import os
from . import mail, mail_api_client


def send_email(to, subject, template):
    message = mail(
        from_email=os.getenv("MAIL_DEFAULT_SENDER"),
        to_emails=to,
        subject=subject,
        html_content=template)
    try:
        sg = mail_api_client
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# from flask import Flask, current_app
# from project.config import Config
# from flask_mail import Message, Mail
# from . import mail


# def send_email(to, subject, template):
#     """General send mail function. Takes 'to', 'subject' and 'template' """
#
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=os.getenv("MAIL_DEFAULT_SENDER")
#     )
#     mail.send(msg)
