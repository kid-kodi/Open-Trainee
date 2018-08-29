# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import home
from ..models import User, Trainee


@home.route('/')
def dashboard():
    """
    Render the homepage template on the / route
    """
    user = User.query.all()
    trainee = Trainee.query.all()
    return render_template('home/index.html', user=user, trainee=trainee, title="Welcome")