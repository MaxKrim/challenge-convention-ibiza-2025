import os
from flask import Flask
from src.models import db
from src.routes.inscription import inscription_bp
from src.routes.collecte import collecte_bp
from src.routes.scoring import scoring_bp
from src.routes.dashboard import dashboard_bp
from src.routes.admin import admin_bp
from src.routes import routes_bp

def create_app():
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'challenge_convention_ibiza_2025')
    
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///challenge.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation de la base de données
    db.init_app(app)
    
    # Enregistrement des blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(inscription_bp)
    app.register_blueprint(collecte_bp)
    app.register_blueprint(scoring_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    
    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
