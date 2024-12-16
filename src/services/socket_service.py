from flask_socketio import SocketIO, emit, disconnect
from flask_jwt_extended import decode_token
from flask import request

class SocketService:
    def __init__(self, app=None):
        self.user_sessions = {}  # Map of user IDs to session IDs
        self.app = app
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
            with self.app.app_context():
                decoded = decode_token(token)
                self.app.logger.info(f"Decoded token: {decoded}")  # Log the decoded token to debug
                return decoded  # Return the entire decoded token for further inspection
        except Exception as e:
            self.app.logger.error(f"Invalid token: {e}")
            return None

    def handle_connect(self, token):
        """
        Handle client connection and validate JWT token.
        The token should be passed explicitly from the client.
        """
        # Ensure token is passed in the query string
        token = request.args.get('token')
        if token:
            decoded_token = self.validate_token(token)
            if decoded_token:
                user_id = decoded_token.get('sub')
                if user_id:
                    self.user_sessions[user_id] = request.sid
                    self.app.logger.info(f"User {user_id} connected with session ID {request.sid}")
                    emit('server_message', {'message': 'Welcome to the chat server!'})
                else:
                    self.app.logger.warning('User ID not found in token')
                    disconnect()
            else:
                self.app.logger.warning('Unauthorized connection attempt')
                disconnect()

    def handle_disconnect(self):
        """
        Handle client disconnection.
        """
        user_id = None
        for uid, sid in self.user_sessions.items():
            with self.app.app_context():
                if sid == request.sid:
                    user_id = uid
                    break
        if user_id:
            del self.user_sessions[user_id]
            self.app.logger.info(f"User {user_id} disconnected")

    def handle_send_message(self, data):
        """
        Route messages to all connected users (broadcast to everyone).
        The token should be passed explicitly from the client (via query args).
        """
        # Get the token from query args
        token = request.args.get('token')  # Extract token from the query parameters
        
        # If no token is provided in the query, return an error and disconnect
        if not token:
            self.app.logger.warning('Token missing in query args')
            disconnect()
            return

        # Validate the token
        decoded_token = self.validate_token(token)
        
        if decoded_token:
            # Broadcast the message to all connected clients
            emit('receive_message', data, broadcast=True)
        else:
            self.app.logger.warning('Unauthorized attempt to send a message')
            disconnect()

    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(self.app, debug=True, host=host, port=port)