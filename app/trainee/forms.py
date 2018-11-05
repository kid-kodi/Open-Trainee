# app/departement/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from app import images

class SearchForm(FlaskForm):
    first_name = StringField('Nom')
    last_name = StringField('Prénom')
    unit_id = SelectField('Unité de recherche', choices=[], coerce=int)
    submit = SubmitField('Chercher')

class TraineeForm(FlaskForm):
    """
    Form for departement to add or edit a trainee
    """
    image = FileField('Image', validators=[FileAllowed(images, 'Images only')])
    registration_number = HiddenField(validators=[DataRequired()])
    first_name = StringField('Nom', validators=[DataRequired()])
    last_name = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Mail', validators=[DataRequired(), Email()])
    phone = StringField('Numéro', validators=[DataRequired()])
    birthdate = StringField('Date de naissance', validators=[DataRequired()])

    school = StringField('Ecole', validators=[DataRequired()])
    diplome = StringField('Diplome', validators=[DataRequired()])
    spinneret_id = SelectField(choices=[], coerce=int, label="Filière")
    level_id = SelectField(choices=[], coerce=int, label="Niveau")

    unit_id = SelectField(choices=[], coerce=int, label="Unité")
    responsable = StringField('Responsable')
    started_date = StringField('Date de debut')
    ended_date = StringField('Date de fin')
    apply_date = StringField('date application')
    theme = StringField('Thème')

    submit = SubmitField('Soumettre')
