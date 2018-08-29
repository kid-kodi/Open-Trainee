# app/models.py
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

basedir = os.path.abspath(os.path.dirname(__file__))

class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    units = db.relationship('Unit', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Unit(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    departement_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    trainees = db.relationship('Trainee', backref='unit',
                                lazy='dynamic')

    def __repr__(self):
        return '<Unit: {}>'.format(self.name)


class Spinneret(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'spinnerets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    trainees = db.relationship('Trainee', backref='spinneret')

    def __repr__(self):
        return '<Spinneret: {}>'.format(self.name)


class Level(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    trainees = db.relationship('Trainee', backref='level')

    def __repr__(self):
        return '<Level: {}>'.format(self.name)


class Trainee(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'trainees'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), index=True, unique=True)
    phone = db.Column(db.String(255), index=True, unique=True)
    birthdate = db.Column(db.String, unique=True)
    school = db.Column(db.String)
    diplome = db.Column(db.String)
    spinneret_id = db.Column(db.Integer, db.ForeignKey('spinnerets.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    responsable = db.Column(db.String)
    started_date = db.Column(db.String)
    ended_date = db.Column(db.String)
    apply_date = db.Column(db.String)
    theme = db.Column(db.String)

    def __repr__(self):
        return '<Trainee: {}>'.format(self.first_name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Seed:
    @staticmethod
    def start():
        level_list = [
        Level(name='BTS', description=''),
        Level(name='MASTER', description=''),
        Level(name='MASTER2', description=''),
        Level(name='THESE D\'EXERCISE', description=''),
        Level(name='THESE UNIQUE', description='')]

        for lvl in level_list:
            db.session.add(lvl)
        db.session.commit()