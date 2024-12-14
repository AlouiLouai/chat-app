from flask_jwt_extended import get_jwt_identity
from src.models.user import User
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from src.services.bucket_service import BucketService

class UserService:
    def __init__(self, db):
        self.db = db
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY is not set in the configuration.")
        
    def get_users(self, current_user):
        """
        Retrieve all users except the currently connected user.
        """
        try:
            # Retrieve all users except the one matching the current user's username
            users = User.query.filter(User.username != current_user).all()
            # Return the list of users
            return [user.to_dict() for user in users]
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
        
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
        
    
    def update_profile(self, username, data, file=None):
        """
        Updates the user's profile details, including uploading a profile picture.
        """
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                return False, "User not found."
            
            # Update user details
            if "email" in data:
                user.email = data["email"]
                
            # Initialize BucketService instance
            bucket_service = BucketService()

            # Upload the profile picture if provided
            if file:
                upload_result = bucket_service.upload_image(file)
                print(f"upload_result {upload_result}")
                if not upload_result["success"]:
                    return False, upload_result["error"]
                # Save the uploaded image URL to the user's profile
                user.image_url = upload_result["url"]

            # Commit the updates to the database
            self.db.session.commit()
            return True, "Profile updated successfully."
        except SQLAlchemyError as e:
            self.db.session.rollback()  # Rollback in case of a database error
            current_app.logger.error(f"Error in update_profile: {str(e)}")
            return False, "An error occurred while updating the profile."
        except Exception as e:
            current_app.logger.error(f"Error in update_profile: {str(e)}")
            return False, "An unexpected error occurred."
