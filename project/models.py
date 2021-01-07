from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'user'
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
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    babies = db.relationship('Baby', backref='user', lazy=True,)

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

    __tablename__ = 'baby'
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
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'),)
    images = db.relationship('BabyImg', backref='baby', lazy=True,)

    def __repr__(self):
        return '<Baby {}>'.format(self.name)


class BabyImg(db.Model):
    """Baby picture model"""

    __tablename__ = 'babyimg'
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
    filename = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    baby_id = db.Column(db.Integer, db.ForeignKey('baby.id'))

    def __repr__(self):
        return '<Img {}>'.format(self.filename)
