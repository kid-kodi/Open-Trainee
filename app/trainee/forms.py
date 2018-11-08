# app/departement/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from app import images

class SearchForm(FlaskForm):
    first_name = StringField('first name')
    last_name = StringField('last name')
    unit_id = SelectField('Search unit', choices=[], coerce=int)
    submit = SubmitField('Search')

class TraineeForm(FlaskForm):
    """
    Form for departement to add or edit a trainee
    """
    image = FileField('Image', validators=[FileAllowed(images, 'Images seulement')])
    registration_number = HiddenField(validators=[DataRequired()])
    first_name = StringField('Nom', validators=[DataRequired()])
    last_name = StringField('Prénoms', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    birthdate = StringField('Date de naissance', validators=[DataRequired()])

    school = StringField('Etablissement', validators=[DataRequired()])
    diplome = StringField('Diplôme Obtenu', validators=[DataRequired()])
    spinneret_id = SelectField(choices=[], coerce=int, label="Filière")
    level_id = SelectField(choices=[], coerce=int, label="Niveau d'étude")

    unit_id = SelectField(choices=[], coerce=int, label="Unité")
    responsable = StringField('Responsable')
    started_date = StringField('Date de début de stage')
    ended_date = StringField('Date de fin de stage')
    theme = StringField('Thème')
    apply_date = StringField('Date de soutenance')

    submit = SubmitField('Enregistrer')
