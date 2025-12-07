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
            # Seed sample data if DB is empty or incomplete
            try:
                from .models import User, Club, Event
                import datetime
                import random

                # 1. Ensure Users Exist
                admin = User.query.filter_by(username='admin').first()
                if not admin:
                    admin = User(username='admin', email='admin@example.com', role='admin')
                    admin.set_password('adminpass')
                    db.session.add(admin)
                    db.session.commit()

                users = [admin]
                user_names = ['alice', 'berat', 'efe', 'mehmet', 'ayse', 'fatma', 'ali', 'veli', 'zeynep', 'can']
                
                for name in user_names:
                    u = User.query.filter_by(username=name).first()
                    if not u:
                        u = User(username=name, email=f'{name}@example.com')
                        u.set_password('password123')
                        db.session.add(u)
                    users.append(u)
                db.session.commit()
                
                all_users = User.query.all()

                # 2. Sync Clubs (Create needed, Update existing, Delete unwanted)
                target_clubs = [
                    {'name': 'Bilişim ve Teknoloji Kulübü', 'desc': 'Yazılım, donanım ve teknoloji çalışmalarına odaklı kulüp.', 'img': 'teknoloji.jpg'},
                    {'name': 'Spor ve Yaşam Kulübü', 'desc': 'Farklı spor dallarında etkinlikler ve turnuvalar.', 'img': 'spor.jpg'},
                    {'name': 'Güzel Sanatlar Kulübü', 'desc': 'Resim ve heykel çalışmaları.', 'img': 'sanat.jpg'},
                    {'name': 'Müzik Topluluğu', 'desc': 'Müzik pratikleri, konserler ve performanslar.', 'img': 'muzik.jpg'},
                    {'name': 'Edebiyat ve Kültür Kulübü', 'desc': 'Okuma grupları ve edebi etkinlikler.', 'img': 'edebiyat.jpg'},
                    {'name': 'Sahne Sanatları Kulübü', 'desc': 'Sahne sanatları ve oyunculuk atölyeleri.', 'img': 'tiyatro.jpg'}
                ]
                
                target_names = [c['name'] for c in target_clubs]
                
                # Delete clubs not in target list
                existing_clubs = Club.query.all()
                for club in existing_clubs:
                    if club.name not in target_names:
                        Event.query.filter_by(club_id=club.id).delete()
                        club.members = []
                        db.session.delete(club)
                db.session.commit()
                
                # Create or Update target clubs
                for data in target_clubs:
                    club = Club.query.filter_by(name=data['name']).first()
                    image_path = f'/static/img/{data["img"]}'
                    
                    if club:
                        club.description = data['desc']
                        club.image_url = image_path
                    else:
                        president = random.choice(all_users)
                        club = Club(
                            name=data['name'],
                            description=data['desc'],
                            image_url=image_path,
                            president_id=president.id
                        )
                        db.session.add(club)
                    db.session.commit()

                # 3. Ensure Events and Members Exist
                clubs = Club.query.all()
                for club in clubs:
                    # Ensure at least 1 event
                    if not club.events:
                        for j in range(random.randint(1, 2)):
                            days_offset = random.randint(5, 30)
                            ev = Event(
                                name=f'{club.name} Etkinliği {j+1}', 
                                description=f'{club.name} tarafından düzenlenen harika bir etkinlik.', 
                                date=datetime.datetime.now() + datetime.timedelta(days=days_offset), 
                                location='Kampüs Merkezi', 
                                club_id=club.id, 
                                image_url=club.image_url
                            )
                            db.session.add(ev)
                    
                    # Ensure some members
                    if not club.members:
                        potential_members = [u for u in all_users if u.id != club.president_id]
                        if potential_members:
                            members_to_add = random.sample(potential_members, k=min(len(potential_members), random.randint(3, 6)))
                            for m in members_to_add:
                                club.members.append(m)
                    
                    db.session.commit()

            except Exception:
                import traceback
                traceback.print_exc()
        except Exception as e:
            print(f"Error during app initialization: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    return app
