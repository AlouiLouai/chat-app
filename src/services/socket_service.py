from flask_socketio import SocketIO, emit, disconnect
from flask_jwt_extended import decode_token
from flask import current_app, request, app

class SocketService:
    def __init__(self, app=None):
        self.user_sessions = {}  # Map of user IDs to session IDs
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

    def validate_token(self, token):
        """
        Validate the JWT token provided by the client and return the decoded token.
        This function will ensure the app context is pushed for token decoding.
        """
        try:
            # Explicitly push the app context before calling decode_token
            with current_app.app_context():
                decoded = decode_token(token)
                current_app.logger.info(f"Decoded token: {decoded}")  # Log the decoded token to debug
                return decoded  # Return the entire decoded token for further inspection
        except Exception as e:
            current_app.logger.error(f"Invalid token: {e}")
            return None

    def handle_connect(self):
        """
        Handle client connection and validate JWT token.
        """
        token = request.args.get('token')
        decoded_token = self.validate_token(token)
        
        if decoded_token:
            # Extract the user ID from the decoded token, assuming 'identity' is a key in the token
            user_id = decoded_token.get('sub') 
            if user_id:
                self.user_sessions[user_id] = request.sid
                current_app.logger.info(f"User {user_id} connected with session ID {request.sid}")
                emit('server_message', {'message': 'Welcome to the chat server!'})
            else:
                current_app.logger.warning('User ID not found in token')
                disconnect()
        else:
            current_app.logger.warning('Unauthorized connection attempt')
            disconnect()

    def handle_disconnect(self):
        """
        Handle client disconnection.
        """
        user_id = None
        for uid, sid in self.user_sessions.items():
            if sid == request.sid:
                user_id = uid
                break
        if user_id:
            del self.user_sessions[user_id]
            current_app.logger.info(f"User {user_id} disconnected")

    def handle_send_message(self, data):
        """
        Route messages to all connected users (broadcast to everyone).
        """
        token = request.args.get('token')
        decoded_token = self.validate_token(token)
        
        if decoded_token:
            # Broadcast the message to all connected clients
            emit('receive_message', data, broadcast=True)
        else:
            current_app.logger.warning('Unauthorized attempt to send a message')
            disconnect()

    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(current_app, debug=True, host=host, port=port)
