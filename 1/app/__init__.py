import os
from flask import Flask, url_for
from sqlalchemy import text, inspect
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
            # Ensure new columns exist on existing DB (simple ALTER for SQLite)
            try:
                inspector = inspect(db.engine)
                cols = [c['name'] for c in inspector.get_columns('club')]
                if 'image_url' not in cols:
                    with db.engine.begin() as conn:
                        conn.execute(text("ALTER TABLE club ADD COLUMN image_url VARCHAR(255)"))
            except Exception:
                # If introspection or ALTER fails, continue quietly — seeding will handle missing columns
                import traceback
                traceback.print_exc()
            # Seed sample data if DB is empty
            try:
                from .models import User, Club, Event
                # If there are no clubs, create sample users, clubs and events
                if Club.query.count() == 0:
                    import datetime

                    admin = User(username='admin', email='admin@example.com', role='admin')
                    admin.set_password('adminpass')

                    user1 = User(username='alice', email='alice@example.com')
                    user1.set_password('password1')
                    user2 = User(username='berat', email='berat@example.com')
                    user2.set_password('password2')
                    user3 = User(username='efe', email='efe@example.com')
                    user3.set_password('password3')

                    db.session.add_all([admin, user1, user2, user3])
                    db.session.commit()

                    # Create clubs with image urls pointing to static images
                    clubs = [
                        Club(name='Teknoloji Kulübü', description='Yazılım, donanım ve teknoloji çalışmalarına odaklı kulüp.', image_url=url_for('static', filename='img/club1.svg'), president_id=admin.id),
                        Club(name='Spor Kulübü', description='Farklı spor dallarında etkinlikler ve turnuvalar.', image_url=url_for('static', filename='img/club2.svg'), president_id=user1.id),
                        Club(name='Sanat Kulübü', description='Resim, heykel ve atölye çalışmaları.', image_url=url_for('static', filename='img/club3.svg'), president_id=user2.id),
                        Club(name='Müzik Kulübü', description='Müzik pratikleri, konserler ve performanslar.', image_url=url_for('static', filename='img/club4.svg'), president_id=user3.id),
                        Club(name='Edebiyat Kulübü', description='Okuma grupları ve edebi etkinlikler.', image_url=url_for('static', filename='img/club5.svg'), president_id=user1.id),
                    ]
                    db.session.add_all(clubs)
                    db.session.commit()

                    # Helper to create events
                    def make_event(club, name, days_offset):
                        ev = Event(name=name, description=f'{name} açıklaması', date=datetime.datetime.now() + datetime.timedelta(days=days_offset), location='Kampüs Binası', club_id=club.id, image_url=club.image_url)
                        db.session.add(ev)
                        return ev

                    events = []
                    for idx, c in enumerate(Club.query.all(), start=1):
                        ev = make_event(c, f'{c.name} - İlk Etkinlik', idx * 7)
                        events.append(ev)

                    db.session.commit()
                    # Add members to clubs
                    all_users = User.query.filter(User.username.in_(['admin','alice','berat','efe'])).all()
                    for c in Club.query.all():
                        for u in all_users[:3]:
                            c.members.append(u)
                    db.session.commit()
            except Exception:
                # Seeding should not break app init on errors
                import traceback
                traceback.print_exc()
        except Exception as e:
            print(f"Error during app initialization: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    return app
