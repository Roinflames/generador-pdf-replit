# In your __init__.py or wherever you create the main blueprint
from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from . import routes