from flask import Blueprint

prediction = Blueprint('prediction', __name__)

from . import views
