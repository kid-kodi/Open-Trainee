from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CustomerForm(FlaskForm):
    display_as = StringField('Raison sociale', validators=[DataRequired()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')