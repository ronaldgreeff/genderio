from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Optional
)

class BabyForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[Optional()]
    )
    dob = DateTimeField(
        'Date of Birth',
        validators=[
            DataRequired()
        ]
    )
    gender = StringField(
        'Gender',
        validators=[DataRequired()]
    )
    submit = SubmitField('Predict')
