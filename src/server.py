import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from src.controllers.auth_controller import auth_controller
from src.database import DatabaseService, db
from flask_cors import CORS
from src.models.user import User
from src.services.socket_service import SocketService

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")


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
socketio = SocketIO(app, cors_allowed_origins=[os.getenv("FRONTEND_APP")])

# Enable CORS for the auth controller only
#CORS(auth_controller, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app, origins=[os.getenv("FRONTEND_APP")])

socket_service = SocketService(app)

jwt = JWTManager(app)

# Register the auth_controller blueprint with the app
app.register_blueprint(auth_controller, url_prefix='/auth')

@app.route("/")
def index():
    return jsonify({'message': 'Chat server is running!'})

if __name__ == "__main__":
    socket_service.run()