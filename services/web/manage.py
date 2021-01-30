import os
from datetime import datetime as dt
from flask.cli import FlaskGroup
from project import create_app  # from project import app, db, User
from project.models import db, User

# app = create_app(os.getenv('FLASK_ENV') or 'default')
app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        name="Ron",
        email="a@a.com",
        created_on=dt.now(),
        confirmed=1
    )
    user.set_password("asdfgh")
    db.session.commit()


if __name__ == "__main__":
    cli()
