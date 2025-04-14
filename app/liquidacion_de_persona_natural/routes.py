from flask import render_template
from . import liquidacion_bp

@liquidacion_bp.route('/liquidacion')
def liquidacion_view():
    # return render_template('liquidacion_de_persona_natural/liquidacion.html')
    return "En construcciòn"
