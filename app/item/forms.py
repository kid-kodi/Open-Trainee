from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    category = SelectField('Selectionner une Catégorie', coerce=int, choices=[(1, 'Produit'), (2, 'Service')])
    name = StringField('Nom', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    selling_price = StringField('Prix de vente', validators=[DataRequired()])
    buying_price = StringField('Prix d\'achat', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')