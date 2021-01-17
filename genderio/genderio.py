import os
import sys
from datetime import date, timedelta
from dotenv import load_dotenv
import click
from flask import Flask
# from app.tokens import generate_outcome_token

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
        Baby.id,
    ).join(
        Baby
    ).filter(
        Baby.dob.between(a_week_ago, date.today()),
    ).all()

    token = generate_outcome_token(parent_email, baby_id)
    url = url_for('', token=token, _external=True)
    YOU ARE HERE

    # todo: generate email with token and query params
    # (for predicted outcome)
