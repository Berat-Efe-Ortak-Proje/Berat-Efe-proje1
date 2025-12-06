import os, sys
repo_root = os.path.dirname(os.path.dirname(__file__))
# Add '1' package to path so we can import the Flask app package
sys.path.insert(0, os.path.join(repo_root, '1'))

from app import create_app

print('Creating app (this will also run seeding if DB is empty)...')
app = create_app()

with app.app_context():
    from app.models import Club, User
    club_count = Club.query.count()
    user_count = User.query.count()
    print(f'Clubs in DB: {club_count}')
    print(f'Users in DB: {user_count}')
    if club_count:
        c = Club.query.first()
        print('First club:', c.name)
        print('image_url field value:', c.image_url)
        # Try to resolve the static file path
        filename = os.path.basename(c.image_url) if c.image_url else None
        if filename:
            static_path = os.path.join(app.static_folder, 'img', filename)
            print('Expected static path:', static_path)
            print('Static file exists:', os.path.exists(static_path))
    else:
        print('No clubs found after seeding.')

print('Check complete.')
