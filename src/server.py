from flask import Flask
from src.database import DatabaseService, db

app = Flask(__name__)

# Initialize db with the app
db_service = DatabaseService(app)

# Create the database tables if they don't exist
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating database tables: {e}")

@app.route("/")
def hello():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)