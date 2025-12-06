import os, sys
repo_root = os.path.dirname(os.path.dirname(__file__))
# Add '1' package to path so we can import the Flask app package
sys.path.insert(0, os.path.join(repo_root, '1'))

from app import create_app
from flask import url_for

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

    # Check hero images
    print('\nChecking hero images...')
    for i in range(1, 5):
        fname = f'hero{i}.svg'
        fpath = os.path.join(app.static_folder, 'img', fname)
        exists = os.path.exists(fpath)
        print(f'{fname}: {"Exists" if exists else "MISSING"} at {fpath}')
        if exists:
            with app.test_request_context():
                url = url_for('static', filename=f'img/{fname}')
                print(f'  URL generated: {url}')

print('Check complete.')
