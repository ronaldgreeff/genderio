import os
import sys
from datetime import date, timedelta
from dotenv import load_dotenv
import click
from flask import Flask, url_for, render_template
from app.prediction.tokens import generate_outcome_token

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db, mail
from app.models import User, Baby, BabyImg

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def scheduled():
    """Schedule (cron) run every Friday 10am"""
    a_week_ago = date.today() - timedelta(days=7)

    emails = db.session.query(
        User.email,
        User.name,
        Baby,
    ).join(
        Baby
    ).filter(
        Baby.dob.between(a_week_ago, date.today()),
        Baby.last_outcome_email == None,
        Baby.gender == 'u',
        Baby.predicted_gender != 'u',
    ).all()

    print(emails)

    for parent_email, user_name, baby in emails:

        data = {
            'user_name': user_name,
        }

        if baby.name:
            data['baby_name'] = baby.name
        else:
            data['dob'] = baby.dob

        token = generate_outcome_token(parent_email, baby.id)
        confirm_url = url_for('prediction.confirm_outcome', token=token, _external=True)
        html = render_template(
            'gender_confirm.html',
            confirm_url=confirm_url,
            data=data,
        )
        subject = "Did we get it right?"

        print(confirm_url)

        # send_email(parent_email, subject, html)

    # url = url_for('', token=token, _external=True)
    # # YOU ARE HERE

    # todo: generate email with token and query params
    # (for predicted outcome)
