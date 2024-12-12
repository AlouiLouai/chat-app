from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from flask import current_app, request
from collections import defaultdict

class SocketService:
    def __init__(self, app=None):
        self.user_sessions = {}  # Map of user IDs to session IDs
        self.channel_users = defaultdict(set)  # Map of channel names to user IDs
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
        self.socketio.on_event('join_channel', self.handle_join_channel)
        self.socketio.on_event('leave_channel', self.handle_leave_channel)

    def validate_token(self, token):
        """
        Validate the JWT token provided by the client.
        """
        try:
            decoded = decode_token(token)
            return decoded.get('identity') # identity as user ID
        except Exception as e:
            current_app.logger.error(f"Invalid token: {e}")
            return None

    def handle_connect(self):
        """
        Handle client connection and validate JWT token.
        """
        token = request.args.get('token')
        user_id = self.validate_token(token)
        if user_id:
            self.user_sessions[user_id] = request.sid
            current_app.logger.info(f"User {user_id} connected with session ID {request.sid}")
            emit('server_message', {'message': 'Welcome to the chat server!'})
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
            for channel, users in self.channel_users.items():
                users.discard(user_id)
            current_app.logger.info(f"User {user_id} disconnected")


    def handle_join_channel(self, data):
        """
        Allow users to join a specific channel.
        """
        token = request.args.get('token')
        user_id = self.validate_token(token)
        if user_id:
            channel = data.get('channel')
            if channel:
                self.channel_users[channel].add(user_id)
                join_room(channel)
                current_app.logger.info(f"User {user_id} joined channel {channel}")
                emit('server_message', {'message': f'You joined channel {channel}'}, room=request.sid)
        else:
            current_app.logger.warning('Unauthorized attempt to join channel')
            disconnect()

    def handle_leave_channel(self, data):
        """
        Allow users to leave a specific channel.
        """
        token = request.args.get('token')
        user_id = self.validate_token(token)
        if user_id:
            channel = data.get('channel')
            if channel and user_id in self.channel_users[channel]:
                self.channel_users[channel].remove(user_id)
                leave_room(channel)
                current_app.logger.info(f"User {user_id} left channel {channel}")
                emit('server_message', {'message': f'You left channel {channel}'}, room=request.sid)

    def handle_send_message(self, data):
        """
        Route messages to a specific channel or private user.
        """
        token = request.args.get('token')
        user_id = self.validate_token(token)
        if user_id:
            recipient_channel = data.get('channel')
            recipient_user = data.get('recipient_user')
            message = data.get('message')

            if recipient_channel:
                # Broadcast message to the channel
                current_app.logger.info(f"User {user_id} sent message to channel {recipient_channel}: {message}")
                emit('receive_message', {'user_id': user_id, 'message': message}, room=recipient_channel)
            elif recipient_user:
                # Send private message to the recipient user
                recipient_sid = self.user_sessions.get(recipient_user)
                if recipient_sid:
                    current_app.logger.info(f"User {user_id} sent private message to user {recipient_user}: {message}")
                    emit('receive_message', {'user_id': user_id, 'message': message}, room=recipient_sid)
                else:
                    current_app.logger.warning(f"Private message failed: User {recipient_user} not connected")
            else:
                current_app.logger.warning("Message must specify a channel or recipient user")
        else:
            current_app.logger.warning('Unauthorized attempt to send a message')
            disconnect()
    
    def run(self, host='0.0.0.0', port=5000):
        """
        Run the SocketIO server.
        """
        self.socketio.run(current_app, debug=True, host=host, port=port)
