from flask_socketio import SocketIO
from flask import current_app
from flask_socketio import emit

class SocketService:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize the SocketIO app with CORS and other settings.
        """
        self.socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])
        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('disconnect', self.handle_disconnect)
        self.socketio.on_event('send_message', self.handle_send_message)

    def handle_connect(self):
        print('A user connected')
        emit('server_message', {'message': 'Welcome to the chat server!'})

    def handle_disconnect(self):
        print('A user disconnected')

    def handle_send_message(self, data):
        """
        Listen for a 'send_message' event from a client and broadcast it to everyone.
        """
        print(f"Message received: {data}")
        emit('receive_message', data, broadcast=True)
    
    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(current_app, debug=True, host=host, port=port)
