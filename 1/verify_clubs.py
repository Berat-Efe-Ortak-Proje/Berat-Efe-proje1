from app import create_app, db
from app.models import Club

app = create_app()
with app.app_context():
    clubs = Club.query.all()
    print(f"Total clubs: {len(clubs)}")
    for c in clubs:
        print(f"- {c.name}")
