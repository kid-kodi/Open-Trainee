# app/departement/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from app import images

class TraineeForm(FlaskForm):
    """
    Form for departement to add or edit a trainee
    """
    image = FileField('Image', validators=[FileAllowed(images, 'Images only')])
    registration_number = HiddenField(validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    birthdate = StringField('Birth date', validators=[DataRequired()])

    school = StringField('School', validators=[DataRequired()])
    diplome = StringField('Diplome', validators=[DataRequired()])
    spinneret_id = SelectField(choices=[], coerce=int, label="Spinneret")
    level_id = SelectField(choices=[], coerce=int, label="Level")

    unit_id = SelectField(choices=[], coerce=int, label="Unit")
    responsable = StringField('Responsable')
    started_date = StringField('Started date')
    ended_date = StringField('Ended date')
    apply_date = StringField('Apply date')
    theme = StringField('Theme')

    submit = SubmitField('Submit')