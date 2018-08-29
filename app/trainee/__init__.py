from flask import Blueprint

trainee = Blueprint('trainee', __name__)

from . import routes