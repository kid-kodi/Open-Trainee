from flask import Blueprint

bp = Blueprint('purchase', __name__)

from . import routes, forms