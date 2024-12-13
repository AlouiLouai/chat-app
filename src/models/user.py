from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db
from datetime import datetime, timezone

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_seen = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    
     # New field for storing image URL
    image_url = Column(String(255), nullable=True)
    
     # Relationship with Token
    tokens = relationship('Token', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        """
        Hash the password using a strong algorithm (e.g., pbkdf2:sha256).
        Werkzeug automatically handles salting.
        """
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password):
        """
        Verify the hashed password matches the provided password.
        """
        return check_password_hash(self.password_hash, password)

    def deactivate(self):
        """
        Mark a user as inactive (soft delete).
        """
        self.is_active = False

    def update_last_seen(self):
        """
        Update the `last_seen` timestamp.
        """
        self.last_seen = datetime.now(timezone.utc)
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image_url": self.image_url,
            "last_seen": self.last_seen,  # Example, include relevant fields here
        }