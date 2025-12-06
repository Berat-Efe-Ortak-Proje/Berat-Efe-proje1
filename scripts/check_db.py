import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '1'))
from app import create_app, db
from app.models import Club

app = create_app()
with app.app_context():
    clubs = Club.query.all()
    print(f"Total clubs: {len(clubs)}")
    for c in clubs:
        print(f"Club: {c.name}, Desc: {c.description}")
