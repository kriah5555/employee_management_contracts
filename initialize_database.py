from database import app, db
from models import *

def initialize_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    initialize_database()
    print("Database initialized.")