from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import db
from datetime import datetime, timezone

class Token(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    refresh_token = Column(String(512), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expired_at = Column(DateTime, nullable=False)  # When the refresh token will expire

    user = relationship('User', back_populates='tokens')

    def __repr__(self):
        return f'<Token {self.refresh_token}>'