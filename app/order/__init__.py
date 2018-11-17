from flask import Blueprint

bp = Blueprint('order', __name__)

from . import routes, forms