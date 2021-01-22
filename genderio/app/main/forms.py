from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, SubmitField, HiddenField,)
from wtforms.validators import (
    DataRequired,
    Email,
    Optional
)

class NewBabyForm(FlaskForm):
    """Add a baby"""
    name = StringField(
        'Name',
        validators=[Optional()]
    )
    dob = DateField(
        'Date of Birth',
        format='%d-%m-%Y',
        validators=[
            DataRequired()
        ]
    )
    add = SubmitField('Add')

class UpdateBabyForm(FlaskForm):
    """Update a baby"""
    id = HiddenField(validators=[
        DataRequired()
    ])
    name = StringField(
        'Name',
        validators=[Optional()]
    )
    dob = DateField(
        'Date of Birth',
        format='%d-%m-%Y',
        validators=[
            DataRequired()
        ]
    )
    update = SubmitField('Update')
    delete = SubmitField('Delete')

class ConfirmationForm(FlaskForm):
    id = HiddenField(validators=[
        DataRequired()
    ])
    right = SubmitField('Right')
    wrong = SubmitField('Wrong')
