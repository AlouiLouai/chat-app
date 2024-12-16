from flask_socketio import SocketIO, emit, disconnect
from flask_jwt_extended import decode_token
from flask import request
from src.helpers.session_manager import SessionManager

class SocketService:
    def __init__(self, app=None):
        self.app = app
        self.socketio = None
        self.session_manager = SessionManager()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the SocketIO app with CORS and other settings.
        """
        self.socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])
        self.register_events()
        
    def register_events(self):
        """
        Register socket event handlers
        """
        @self.socketio.on('connect')
        def on_connect():
            token = request.args.get('token')
            self.handle_connect(token)

        @self.socketio.on('disconnect')
        def on_disconnect():
            self.handle_disconnect()

        @self.socketio.on('send_message')
        def on_send_message(data):
            self.handle_send_message(data)

    def validate_token(self, token):
        """
        Validate the JWT token and return the decoded payload.
        """
        try:
            with self.app.app_context():
                return decode_token(token)
        except Exception as e:
            self.app.logger.error(f"Invalid token: {e}")
            return None

    def handle_connect(self, token):
        """
        Handle new client connection.
        """
        decoded_token = self.validate_token(token)
        if decoded_token:
            user_id = decoded_token.get('sub')
            if user_id:
                self.session_manager.add_session(user_id, request.sid)
                self.app.logger.info(f"User {user_id} connected with SID {request.sid}")
                emit('server_message', {'message': 'Welcome!'}, room=request.sid)
            else:
                self.app.logger.warning('Token does not contain user ID.')
                disconnect()
        else:
            self.app.logger.warning('Unauthorized connection attempt.')
            disconnect()

    def handle_disconnect(self):
        """
        Handle client disconnection.
        """
        user_id = self.session_manager.remove_session(request.sid)
        if user_id:
            self.app.logger.info(f"User {user_id} disconnected.")

    def handle_send_message(self, data):
        """
        Handle message broadcasting.
        """
        token = data.get('token')
        decoded_token = self.validate_token(token)
        if decoded_token:
            emit('receive_message', data, broadcast=True)
        else:
            self.app.logger.warning('Unauthorized message attempt.')
            disconnect()

    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(self.app, debug=True, host=host, port=port)
