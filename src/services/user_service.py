from src.models.user import User
from flask import current_app

class UserService:
    def __init__(self, db):
        self.db = db
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY is not set in the configuration.")
        
    def get_profile(self, id):
        """
        Retrieve the profile of the specified user.
        """
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                return None, "User not found."
            
            # Return the user profile details
            profile = {
                "username": user.username,
                "email": user.email,
                "image_url": user.image_url
            }
            return profile, "Profile retrieved successfully."
        except Exception as e:
            current_app.logger.error(f"Error in get_profile: {str(e)}")
            return None, "An error occured while retrieving the profile."