from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
from . import db


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'parents'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
    )
    confirmed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )
    confirmed_on = db.Column(
        db.DateTime,
        nullable=True,
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
    )
    babies = db.relationship('Baby', backref='parent', lazy=True,)

    # def __init__(self, name, email):
    #     self.name = name
    #     self.email = email
    #     self.created_on = dt.now()

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Baby(db.Model):
    """Baby model"""

    __tablename__ = 'babies'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    dob = db.Column(
        db.Date,
        index=False,
        unique=False,
        nullable=True
    )
    gender = db.Column(
        db.String(1),
        nullable=False,
        unique=False,
        default='u',
    )
    predicted_gender = db.Column(
        db.String(1),
        nullable=False,
        unique=False,
        default='u',
    )
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'),)
    images = db.relationship('BabyImg', backref='baby', lazy=True,)

    def __repr__(self):
        return '<Baby {}>'.format(self.name)


class BabyImg(db.Model):
    """Baby picture model"""

    __tablename__ = 'babypics'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    weeks = db.Column(
        db.Integer,
        unique=False,
        nullable=False,
    )
    days = db.Column(
        db.Integer,
        unique=False,
        nullable=False,
    )
    filepath = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    baby_id = db.Column(db.Integer, db.ForeignKey('babies.id'))

    def __repr__(self):
        return '<Img {}>'.format(self.filename)
