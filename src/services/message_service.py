from src.models.message import Message
from src.models.user import User

class MessageService:
    def __init__(self, db, app):
        self.db = db
        self.app = app
        with self.app.app_context():
            self.secret_key = self.app.config.get('SECRET_KEY')
        
    def get_messages(self):
        """
        Retrieve all messages
        """
        try:
            # Perform a JOIN between Message and User tables using user_id
            results = (
                self.db.session.query(Message.content, User.username)
                .join(User, Message.user_id == User.id) # INNER JOIN
                .order_by(Message.timestamp.asc())
                .all()
            )
            # Transform the query result into a list of dictionaries
            messages_list = [
                {"username": username, "message": content}
                for content, username in results
            ]
            
            # Return the list (no need for jsonify here in the service layer)
            return messages_list
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
        