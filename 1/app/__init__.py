import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Çevresel değişkenlerden ayarları al
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    # Veritabanı URI'sini ayarla (Render için PostgreSQL desteği eklenebilir)
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///club_management.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        try:
            from . import models
            from .routes import auth_bp, club_bp, event_bp, main_bp
            
            app.register_blueprint(auth_bp, url_prefix='/auth')
            app.register_blueprint(club_bp, url_prefix='/club')
            app.register_blueprint(event_bp, url_prefix='/event')
            app.register_blueprint(main_bp)
            
            db.create_all()
        except Exception as e:
            print(f"Error during app initialization: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    return app
