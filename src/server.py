import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_socketio import SocketIO
from src.config import get_config
from src.controllers.user_controller import user_controller
from src.controllers.auth_controller import auth_controller
from src.database import DatabaseService, db
from flask_cors import CORS
from src.models.user import User
from src.services.socket_service import SocketService


app = Flask(__name__)

# Load configuration from the Config class
app.config.from_object(get_config())

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
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins=[os.getenv("FRONTEND_APP")])

# Enable CORS for the auth controller only
#CORS(auth_controller, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app, origins=[os.getenv("FRONTEND_APP")], supports_credentials=True)

socket_service = SocketService(app)

jwt = JWTManager(app)

mail = Mail(app)

with app.app_context():
    try:
        connection = mail.connect()
        print("SMTP connection successful!")
    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")

# Register the auth_controller blueprint with the app
app.register_blueprint(auth_controller, url_prefix='/auth')
app.register_blueprint(user_controller, url_prefix='/user')

@app.route("/")
def index():
    return jsonify({'message': 'Chat server is running!'})

if __name__ == "__main__":
    with app.app_context():
        socket_service.socketio.run(app, host="0.0.0.0", port=5000)