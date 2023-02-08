# home/__init__.py

from flask import Blueprint

auth = Blueprint('home', __name__)

from . import routes
