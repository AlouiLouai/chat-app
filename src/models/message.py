from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import db

class Message(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Assuming you have a User model
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='messages')  # Set up reverse relationship

    def __repr__(self):
        return f'<Message {self.id} from {self.user_id} at {self.timestamp}>'