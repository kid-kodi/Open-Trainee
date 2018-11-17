from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SupplierForm(FlaskForm):
    display_as = StringField('Raison sociale', validators=[DataRequired()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')