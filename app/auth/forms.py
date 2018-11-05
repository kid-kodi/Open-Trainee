# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Mail', validators=[DataRequired(), Email()])
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    first_name = StringField('Nom', validators=[DataRequired()])
    last_name = StringField('Prénom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirmez le mot de passe')
    submit = SubmitField('Enrégister')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('cet email est déjà utilisé.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Nom d utilisateur est déjà utilisé.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de pass', validators=[DataRequired()])
    submit = SubmitField('S identifier')