from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, SubmitField, HiddenField,)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
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
        format='%Y-%m-%d',
        validators=[
            DataRequired()
        ]
    )
    add = SubmitField('Add')

class UpdateBabyForm(FlaskForm):
    """Update a baby"""
    id = HiddenField(
        ''
    )
    name = StringField(
        'Name',
        validators=[Optional()]
    )
    dob = DateField(
        'Date of Birth',
        # format='%Y-%m-%d',
        format='%d-%m-%Y',
        validators=[
            DataRequired()
        ]
    )
    update = SubmitField('Update')
    delete = SubmitField('Delete')

class ConfirmationForm(FlaskForm):
    id = HiddenField('')
    right = SubmitField('Right')
    wrong = SubmitField('Wrong')
