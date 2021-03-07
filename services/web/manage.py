import os
from datetime import datetime, date, timedelta
from flask.cli import FlaskGroup
from project import create_app
from project.email import send_email
from project.models import db, User, Baby
from project.prediction.tokens import generate_outcome_token
from flask import send_from_directory, render_template, url_for


app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """ Command to re-create the database """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """ Command to create the first user based on environment variables """
    user = User(
        name=f"{os.getenv('APP_ADMIN_NAME')}",
        email=f"{os.getenv('APP_ADMIN_EMAIL')}",
        created_on=datetime.now(),
        confirmed=1
    )
    user.set_password(f"{os.getenv('APP_ADMIN_PASSWORD')}")
    db.session.add(user)
    db.session.commit()


@cli.command("scheduled")
def scheduled():
    """ Command to run send of scheduled emails """
    a_week_ago = date.today() - timedelta(days=7)

    # Retrieve Parent and Baby details for mail shot
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

    for parent_email, user_name, baby in emails:

        # get the user's name, and the baby's name (which is optional), else dob
        data = {
            'user_name': user_name,
        }

        # use the baby name if it was set else use the dob
        if baby.name:
            data['baby_name'] = baby.name
        else:
            data['dob'] = baby.dob

        # generate email
        token = generate_outcome_token(parent_email, baby.id)
        confirm_url = url_for('prediction.confirm_outcome', token=token, _external=True)
        html = render_template(
            'gender_confirm.html',
            confirm_url=confirm_url,
            data=data,
        )
        subject = "Did we get it right?"

        # send email
        send_email(parent_email, subject, html)

        # set last_outcome_email value
        baby.last_outcome_email = date.today()
        db.session.add(baby)
        db.session.commit()


if __name__ == "__main__":
    cli()
