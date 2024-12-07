from flask import Flask, jsonify
from flask_socketio import SocketIO
from src.database import DatabaseService, db
from flask_cors import CORS
from src.models.user import User
from src.services.socket_service import SocketService

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
    
# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

# Enable CORS for your Next.js app on localhost:3000
CORS(app, origins=["http://localhost:3000"])

socket_service = SocketService(app)

@app.route("/")
def index():
    return jsonify({'message': 'Chat server is running!'})

if __name__ == "__main__":
    socket_service.run()