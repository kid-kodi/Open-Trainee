from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SupplierForm(FlaskForm):
    fournisseur = SelectField('Selectionner un Fournisseur', coerce=int, choices=[(1, ''), (2, '')])
    phone = StringField('Téléphone', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')