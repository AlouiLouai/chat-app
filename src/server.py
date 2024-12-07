from flask import Flask, jsonify
from flask_socketio import SocketIO
from src.database import DatabaseService, db
from flask_cors import CORS
from src.models.user import User

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

@socketio.on('connect')
def handle_connect():
    print('A user connected')
    socketio.emit('server_message', {'message': 'Welcome to the chat server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')
    
@socketio.on('send_message')
def handle_send_message(data):
    """
    Listen for a 'send_message' event from a client and broadcast it to everyone.
    """
    print(f"Message received: {data}")
    socketio.emit('receive_message', data, to=None)

@app.route("/")
def index():
    return jsonify({'message': 'Chat server is running!'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')