import os
from flask.cli import FlaskGroup
from project import create_app  # from project import app, db, User
from project.models import db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(name="Ron", email="a@a.com", password="asdfgh", confirmed=1))
#     db.session.commit()


if __name__ == "__main__":
    cli()
