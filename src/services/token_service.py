import uuid
from datetime import datetime, timedelta
from src.models.token import Token
from flask import current_app

class TokenService:
    @staticmethod
    def generate_refresh_token(user):
        """
        Generates a refresh token using the user's ID and a random string.
        This is an example, and you can modify this for stronger generation methods.
        """
        # Use UUID or any other strategy for secure random string generation
        return str(user.id) + "-" + str(uuid.uuid4())

    @staticmethod
    def store_refresh_token(user, refresh_token):
        """
        Store the generated refresh token in the database with an expiration time.
        """
        try:
            # Set an expiration time for the refresh token (e.g., 30 days)
            expired_at = datetime.now() + timedelta(days=30)

            # Create a new token record and store it
            token = Token(
                user_id=user.id,
                refresh_token=refresh_token,
                expired_at=expired_at
            )
            current_app.db.session.add(token)
            current_app.db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Error storing refresh token: {str(e)}")
            raise

    @staticmethod
    def verify_refresh_token(refresh_token, user):
        """
        Verifies that the provided refresh token is valid and matches the user.
        """
        token = Token.query.filter_by(refresh_token=refresh_token, user_id=user.id).first()

        if token and token.expired_at > datetime.now():
            return True
        return False

    @staticmethod
    def revoke_refresh_token(refresh_token):
        """
        Revoke a specific refresh token (delete it from the database).
        """
        token = Token.query.filter_by(refresh_token=refresh_token).first()
        if token:
            current_app.db.session.delete(token)
            current_app.db.session.commit()
            return True
        return False
