# app/models.py
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login
from app.search import add_to_index, remove_from_index, query_index

basedir = os.path.abspath(os.path.dirname(__file__))

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        print(cls.__tablename__)
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

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
    trainees = db.relationship('Trainee', backref='owner')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String, default=None, nullable=True)
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
@login.user_loader
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
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(200))
    trainees = db.relationship('Trainee', backref='level')

    def __repr__(self):
        return '<Level: {}>'.format(self.name)


class Trainee(SearchableMixin, db.Model):
    __searchable__ = ['first_name', 'last_name' ,'unit_id']

    __tablename__ = 'trainees'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), index=True, unique=True)
    phone = db.Column(db.String(255), index=True, unique=True)
    birthdate = db.Column(db.String)
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
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        json_trainee = {
            'id': self.id,
            'registration_number': self.registration_number,
            'image_filename': self.image_filename,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'birthdate': self.birthdate,
            'school': self.school,
            'diplome': self.diplome,
            'spinneret': self.spinneret.name,
            'level': self.level.name,
            'unit': self.unit.name,
            'responsable': self.responsable,
            'started_date': self.started_date,
            'ended_date': self.ended_date,
            'theme': self.theme
        }
        return json_trainee


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
