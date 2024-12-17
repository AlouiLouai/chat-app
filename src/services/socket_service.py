from flask_socketio import SocketIO, emit, disconnect
from flask_jwt_extended import decode_token
from flask import request
from src.models.message import Message
from src.models.user import User

class SocketService:
    def __init__(self, app=None, db=None):
        self.user_sessions = {}  # Map of user IDs to session IDs
        self.app = app
        self.db = db
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the SocketIO app with CORS and other settings.
        """
        self.socketio = SocketIO(app,logger=True, engineio_logger=True, cors_allowed_origins=["http://localhost:3000"])
        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('disconnect', self.handle_disconnect)
        self.socketio.on_event('send_message', self.handle_send_message)

    def validate_token(self, token):
        """
        Validate the JWT token provided by the client and return the decoded token.
        This function will ensure the app context is pushed for token decoding.
        """
        try:
            # convert the token to bytes before decoding
            token = token.encode('utf-8')
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
        token = request.args.get('token')
        decoded_token = self.validate_token(token)
        
        if decoded_token:
            user_id = decoded_token.get('sub') 
            if user_id:
                with self.app.app_context():
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
        username = data.get('username')  # Retrieve the username
        content = data.get('message')  # Retrieve the message content
        token = request.args.get('token')
        if not token or not username or not content:
            self.app.logger.warning('Invalid data received: Missing username or content')
            disconnect()
            return

        decoded_token = self.validate_token(token)
        if decoded_token:
            user_id = decoded_token.get('sub')
            if user_id:
                # Save and broadcast the message
                try:
                    user = User.query.filter_by(username=user_id).first()
                    if not user:
                        self.app.logger.warning('User not found')
                        disconnect()
                        return
                    
                    new_message = Message(user_id=user.id, content=content)
                    self.db.session.add(new_message)
                    self.db.session.commit()
                    emit('receive_message', {'username': user.username, 'message': content}, broadcast=True)
                except Exception as e:
                    self.app.logger.error(f"Error saving message to database: {e}")
            else:
                self.app.logger.warning('Unauthorized attempt to send a message')
                disconnect()
        else:
            self.app.logger.warning('Invalid or expired token')
            disconnect()

   
    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(self.app, debug=True, host=host, port=port)