import sys
import os

# Add 1/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '1'))

from app import create_app, db
from app.models import Club

app = create_app()

with app.app_context():
    club = Club.query.filter(Club.name == 'Sanat Kulübü').first()
    if club:
        print(f'Updating club: {club.name}')
        print(f'Old description: {club.description}')
        club.description = 'Resim ve heykel çalışmaları.'
        db.session.commit()
        print(f'New description: {club.description}')
    else:
        print('Sanat Kulübü not found.')
