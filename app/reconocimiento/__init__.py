from flask import Blueprint

reconocimiento = Blueprint(
    'reconocimiento',
    __name__, 
    template_folder='templates', 
    static_folder='static'
)

from . import routes