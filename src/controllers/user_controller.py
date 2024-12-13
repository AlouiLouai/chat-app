from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.user import User
from src.services.user_service import UserService
from src.database import db

user_controller = Blueprint('user', __name__)
    
@user_controller.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Endpoint to retrieve the profile of a specified user
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"success": False, "error": "User not found."}), 404

    # Retrieve the user ID from the user object
    user_id = user.id
    # Initialize UserService instance
    user_service = UserService(db=db)
    profile, message = user_service.get_profile(user_id)
    if not profile:
        return jsonify({"success": False, "error": message }), 404
    return jsonify({"success": True, "profile": profile, "message": message}), 200


@user_controller.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Endpoint to update the profile of the authenticated user.
    """
    # Get the current authenticated user from the JWT token
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"success": False, "error": "User not found."}), 404

    # Parse JSON data from the request
    data = request.form.to_dict()
    file = request.files.get("file")  # Optional file for profile picture

    # Initialize UserService instance
    user_service = UserService(db=db)

    # Call the update_profile method
    success, message = user_service.update_profile(username=current_user, data=data, file=file)
    if not success:
        return jsonify({"success": False, "error": message}), 400

    return jsonify({"success": True, "message": message}), 200

@user_controller.route("/users", methods=["GET"])
@jwt_required()
def getUsers():
    """
    Endpoint to get connected users.
    """
    try:
        user_service = UserService(db=db)
        users = user_service.get_users()  # List of users serialized as dictionaries
        return jsonify({"users": users}), 200
    except Exception as e:
        current_app.logger.error(f"Error in getUsers: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
