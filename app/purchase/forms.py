from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
    display_as = StringField('Nom du fourniseur', validators=[DataRequired()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')