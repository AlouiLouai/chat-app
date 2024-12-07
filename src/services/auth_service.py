from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from src.models.user import User
from src.models.token import Token
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

class AuthService:
    def __init__(self, db):
        self.db = db

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
