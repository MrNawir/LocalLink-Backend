from app import app, db

# Initialize the database within the application context
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully.")