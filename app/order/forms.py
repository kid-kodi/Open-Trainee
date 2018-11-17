from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    display_as = StringField('Nom du client', validators=[DataRequired()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')