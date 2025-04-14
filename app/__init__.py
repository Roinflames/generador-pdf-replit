from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from app.models import User  # asegúrate que la ruta sea correcta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.secret_key = 'tu_clave_secreta'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # opcional pero recomendado
    
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    from .auth import auth as auth_bp
    from .main import main as main_bp
    from .reconocimiento import reconocimiento as reconocimiento_bp
    from .generar_informe import generar_informe as informe_bp
    from .diagrama import diagrama_bp as diagrama_bp
    from .escritura_compraventa import escritura_bp as escritura_bp
    from .liquidacion_de_persona_natural import liquidacion_bp as liquidacion_bp
    from .delega_poder import delega_bp as delega_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(reconocimiento_bp, url_prefix='/reconocimiento')
    app.register_blueprint(informe_bp, url_prefix='/informe')
    app.register_blueprint(diagrama_bp, url_prefix='/diagrama')
    app.register_blueprint(escritura_bp, url_prefix='/escritura')
    app.register_blueprint(liquidacion_bp, url_prefix='/liquidacion')
    app.register_blueprint(delega_bp, url_prefix='/delega_poder')

    return app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
