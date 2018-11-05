# app/departement/user.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class userForm(FlaskForm):
    """
    Form for departement to add or edit a user
    """
    email = StringField('Mail', validators=[DataRequired(), Email()])
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    first_name = StringField('Nom', validators=[DataRequired()])
    last_name = StringField('Prénom', validators=[DataRequired()])
    password = PasswordField('Mot de pass', validators=[
                                        DataRequired(),
                                        EqualTo('Confirmer le mot de pass')
                                        ])
    confirm_password = PasswordField('Confirmer le mot de pass')
    submit = SubmitField('Sauver')