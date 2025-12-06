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
                    db.session.commit() # Commit to get ID

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
                
                # Refresh users list with actual DB objects
                all_users = User.query.all()

                # 2. Rename existing clubs to more professional names if needed
                renames = {
                    'Teknoloji Kulübü': 'Bilişim ve Teknoloji Kulübü',
                    'Spor Kulübü': 'Spor ve Yaşam Kulübü',
                    'Sanat Kulübü': 'Güzel Sanatlar Kulübü',
                    'Müzik Kulübü': 'Müzik Topluluğu',
                    'Edebiyat Kulübü': 'Edebiyat ve Kültür Kulübü',
                    'Tiyatro Kulübü': 'Sahne Sanatları Kulübü',
                    'Fotoğrafçılık Kulübü': 'Fotoğrafçılık Topluluğu',
                    'Dans Kulübü': 'Dans Topluluğu',
                    'Girişimcilik Kulübü': 'Girişimcilik ve Kariyer Kulübü',
                    'Doğa ve Gezi Kulübü': 'Doğa Sporları Kulübü'
                }
                
                for old_name, new_name in renames.items():
                    c = Club.query.filter_by(name=old_name).first()
                    if c:
                        c.name = new_name
                        db.session.commit()

                # 3. Remove unwanted clubs
                clubs_to_remove = [
                    'Dans Topluluğu',
                    'Girişimcilik ve Kariyer Kulübü',
                    'Doğa Sporları Kulübü',
                    'Fotoğrafçılık Topluluğu'
                ]
                for name in clubs_to_remove:
                    c = Club.query.filter_by(name=name).first()
                    if c:
                        # Delete associated events first (though cascade might handle it, explicit is safer here without cascade config)
                        Event.query.filter_by(club_id=c.id).delete()
                        # Clear members association
                        c.members = []
                        db.session.delete(c)
                        db.session.commit()

                # 4. Ensure Clubs Exist (with new names) and Update Details
                club_data = [
                    ('Bilişim ve Teknoloji Kulübü', 'Yazılım, donanım ve teknoloji çalışmalarına odaklı kulüp.', 'club1.svg'),
                    ('Spor ve Yaşam Kulübü', 'Farklı spor dallarında etkinlikler ve turnuvalar.', 'club2.svg'),
                    ('Güzel Sanatlar Kulübü', 'Resim ve heykel çalışmaları.', 'club3.svg'),
                    ('Müzik Topluluğu', 'Müzik pratikleri, konserler ve performanslar.', 'club4.svg'),
                    ('Edebiyat ve Kültür Kulübü', 'Okuma grupları ve edebi etkinlikler.', 'club5.svg'),
                    ('Sahne Sanatları Kulübü', 'Sahne sanatları ve oyunculuk atölyeleri.', 'club3.svg')
                ]

                for i, (name, desc, img_file) in enumerate(club_data):
                    club = Club.query.filter_by(name=name).first()
                    if club:
                        # Update existing club details
                        club.description = desc
                        club.image_url = f'/static/img/{img_file}'
                        db.session.commit()
                    else:
                        # Create new club
                        # Pick a random president from users (excluding admin if desired, or just random)
                        president = all_users[i % len(all_users)]
                        
                        club = Club(
                            name=name, 
                            description=desc, 
                            image_url=f'/static/img/{img_file}', 
                            president_id=president.id
                        )
                        db.session.add(club)
                        db.session.commit() # Commit to get ID for events

                        # Create Events for this new club
                        for j in range(random.randint(1, 2)):
                            days_offset = (i + 1) * 3 + (j * 5)
                            ev = Event(
                                name=f'{club.name} Etkinliği {j+1}', 
                                description=f'{club.name} tarafından düzenlenen harika bir etkinlik.', 
                                date=datetime.datetime.now() + datetime.timedelta(days=days_offset), 
                                location='Kampüs Merkezi', 
                                club_id=club.id, 
                                image_url=club.image_url
                            )
                            db.session.add(ev)
                        
                        # Add random members
                        potential_members = [u for u in all_users if u.id != club.president_id]
                        if potential_members:
                            members_to_add = random.sample(potential_members, k=min(len(potential_members), random.randint(3, 6)))
                            for m in members_to_add:
                                club.members.append(m)
                        
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
