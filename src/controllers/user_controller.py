from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.user import User
from src.services.user_service import UserService
from src.database import db

user_controller = Blueprint('user', __name__)

user_service = UserService(db=db,app=current_app)
    
@user_controller.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Endpoint to retrieve the profile of the authenticated user
    """
    current_user = get_jwt_identity()  # Retrieve the current user's username (or ID)
    try:
        profile, message = user_service.get_profile(user_id=current_user)
        if not profile:
            return jsonify({"success": False, "error": message}), 404
        return jsonify({"success": True, "profile": profile, "message": message}), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_profile: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500


@user_controller.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Endpoint to update the profile of the authenticated user.
    """
    current_user = get_jwt_identity()  # Retrieve the current user's username (or ID)
    data = request.form.to_dict()
    file = request.files.get("file")
    
    try:
        success, message = user_service.update_profile(username=current_user, data=data, file=file)
        if not success:
            return jsonify({"success": False, "error": message}), 400
        return jsonify({"success": True, "message": message}), 200
    except Exception as e:
        current_app.logger.error(f"Error in update_profile: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@user_controller.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    Endpoint to get connected users.
    """
    current_user = get_jwt_identity()  # Retrieve the current user's username (or ID)
    try:
        users = user_service.get_users(current_user=current_user)  # Pass the current_user to filter
        return jsonify({"users": users}), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_users: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
