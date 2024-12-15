from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required, set_access_cookies
from src.services.auth_service import AuthService
from src.models.user import User
from src.database import db

auth_controller = Blueprint('auth', __name__)

auth_service = AuthService(db,current_app)

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user, message = auth_service.register(username, email, password)

    if user:
        # Registration successful
        return jsonify({"message": message, "user": {"username": user.username, "email": user.email}}), 201
    # Registration failed
    return jsonify({"message": message}), 400

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    access_token, refresh_token = auth_service.login(username, password)
    if access_token:
        # Create a response object
        response = jsonify({"access_token": access_token, "refresh_token": refresh_token})
        # Set the access token in the cookie
        set_access_cookies(response, access_token)
        # Return the response with the cookie set
        return response, 200
    # If login fails, return an error message
    return jsonify({"message": refresh_token}), 401


@auth_controller.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    success = auth_service.logout(refresh_token)

    if success:
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"message": "Failed to log out"}), 400

@auth_controller.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    success, message = auth_service.forgot_password(email)

    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

@auth_controller.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "New password is required"}), 400

    success, message = auth_service.reset_password(token, new_password)

    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

@auth_controller.route('/test-guard', methods=['GET'])
@jwt_required()
def test_guard():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
        
