import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # instance_relative_config=True allows using the instance folder for DB
    app = Flask(__name__, instance_relative_config=True)

    # Default configs
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # DATABASE_URL can be provided by Render (Postgres) or left empty for SQLite
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Ensure instance folder exists and use it for the SQLite DB file
        try:
            os.makedirs(app.instance_path, exist_ok=True)
        except Exception:
            pass
        db_path = os.path.join(app.instance_path, 'club_management.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

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
