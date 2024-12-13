from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.models.token import Token
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from src.services.email_service import EmailService
from src.services.token_service import TokenService

class AuthService:
    def __init__(self, db):
        self.db = db
        self.email_service = EmailService
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY is not set in the configuration.")
        self.serializer = URLSafeTimedSerializer(secret_key)
        
    def forgot_password(self, email):
        """
        Sends a password reset email to the user.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "Email address not found."

        try:
            # Generate a secure reset token
            reset_token = self.serializer.dumps(email, salt='password-reset-salt')
            reset_url = f'http://localhost:3000/auth/reset-password/{reset_token}'

            # Email content
            subject = "Password Reset Request"
            body = f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."
            html = f"""<p>Hi {user.username},</p>
                       <p>Click the link below to reset your password:</p>
                       <a href="{reset_url}">{reset_url}</a>
                       <p>If you did not request this, please ignore this email.</p>"""

            # Use the EmailService to send the email
            if self.email_service.send_email(subject, [email], body, html):
                return True, "Password reset email sent successfully."
            else:
                return False, "Failed to send password reset email."
        except Exception as e:
            current_app.logger.error(f"Error in forgot_password: {str(e)}")
            return False, "An error occurred. Please try again later."
        
    def reset_password(self, token, new_password):
        """
        Resets the user's password using a valid token.
        """
        try:
            # Validate the reset token
            email = self.serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1-hour expiration
            user = User.query.filter_by(email=email).first()
            if not user:
                return False, "Invalid token or user not found."

            # Update the user's password
            user.set_password(new_password)
            self.db.session.commit()
            return True, "Password reset successfully."
        except Exception as e:
            current_app.logger.error(f"Error in reset_password: {str(e)}")
            return False, "Invalid or expired token."
        
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
        if user and user.check_password(password):
            print("Password is correct, generating tokens...")
            # Mark the user as active
            user.is_active = True
            self.db.session.commit()
            # Create access token (JWT)
            access_token = create_access_token(identity=user.username)
            # Generate refresh token (This should be handled by TokenService)
            refresh_token = TokenService.generate_refresh_token(user)
            if not access_token or not refresh_token:
                print("Error generating tokens")
            else:
                print("Tokens generated successfully")
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
