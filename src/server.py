import os
import signal
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

# Initialize the Flask application directly
app = Flask(__name__)

# Dynamically load the configuration based on FLASK_DEBUG or environment
config_class = get_config()
app.config.from_object(config_class)

# Initialize components
db_service = DatabaseService(app)
jwt = JWTManager(app)
mail = Mail(app)

CORS(app, origins=app.config.get("CORS_ORIGINS", "*"), supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_controller, url_prefix='/auth')
app.register_blueprint(user_controller, url_prefix='/user')

@app.route("/")
def index():
    return jsonify({'message': 'Chat server is running!'})

# Create tables
with app.app_context():
    db.create_all()

# Initialize socket service
socket_service = SocketService(app)

def handle_shutdown(socket_service):
    """
    Gracefully shut down the server.
    """
    def shutdown_signal(signum, frame):
        print("Shutting down server...")
        socket_service.socketio.stop()
    signal.signal(signal.SIGTERM, shutdown_signal)
    signal.signal(signal.SIGINT, shutdown_signal)

if __name__ == "__main__":
    # Handle graceful shutdown
    handle_shutdown(socket_service)

    # Run the socket service
    socket_service.run()
