# app/departement/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UnitForm(FlaskForm):
    """
    Form for departement to add or edit a unit
    """
    name = StringField('Nom', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Sauver')