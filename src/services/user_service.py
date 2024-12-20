from src.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from src.services.bucket_service import BucketService

class UserService:
    def __init__(self, db, app):
        self.db = db
        self.app = app
        with self.app.app_context():
            self.secret_key = self.app.config.get('SECRET_KEY')
        
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
        
    def get_profile(self, username):
        """
        Retrieve the profile of the specified user.
        """
        try:
            user = User.query.filter_by(username=username).first()
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
            self.app.logger.error(f"Error in get_profile: {str(e)}")
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
            self.app.logger.error(f"Error in update_profile: {str(e)}")
            return False, "An error occurred while updating the profile."
        except Exception as e:
            self.app.logger.error(f"Error in update_profile: {str(e)}")
            return False, "An unexpected error occurred."
