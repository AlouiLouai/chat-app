from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.models.token import Token
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from src.services.token_service import TokenService

class AuthService:
    def __init__(self, db):
        self.db = db
        
    def register(self, username, email, password):
        """
        Registers a new user by creating a user record and saving it in the database.
        """
        # Check if the username or email is already taken
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return None, "Username or email is already taken."
        # Create a new user instance
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Set the password hash
        try:
            # Add the new user to the session and commit to save
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user, "User registered successfully."
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error during registration: {str(e)}")
            return None, "An error occurred during registration."

    def login(self, username, password):
        """
        Handles user login by checking credentials and returning access and refresh tokens.
        """
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # Create access token (JWT)
            access_token = create_access_token(identity=user.id)
            # Generate refresh token (This should be handled by TokenService)
            refresh_token = TokenService.generate_refresh_token(user)
            # Store the refresh token in the database
            TokenService.store_refresh_token(user, refresh_token)
            return access_token, refresh_token
        return None, "Invalid username or password"

    def logout(self, refresh_token):
        """
        Handles logout by deleting the provided refresh token from the database.
        """
        try:
            token_record = Token.query.filter_by(refresh_token=refresh_token).first()
            if token_record:
                self.db.session.delete(token_record)
                self.db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error during logout: {str(e)}")
            return False
