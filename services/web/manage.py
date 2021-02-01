import os
from datetime import datetime as dt
from flask.cli import FlaskGroup
from project import create_app
from project.email import send_email
from project.models import db, User
from flask import send_from_directory


app = create_app()
cli = FlaskGroup(app)


@app.cli.command()
def test():
    print('test')


@cli.command("create_db")
# @app.cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        name="test",
        email="a@a.com",
        created_on=dt.now(),
        confirmed=1
    )
    user.set_password("asdfgh")  # TODO: use actual email/password via env vars
    db.session.add(user)
    db.session.commit()


@cli.command("scheduled")
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

        print(data)

        # send_email(parent_email, subject, html)


if __name__ == "__main__":
    cli()
