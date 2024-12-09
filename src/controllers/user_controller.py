import json
from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.user import User
from src.services.user_service import UserService
from src.services.bucket_service import MinioService

user_controller = Blueprint('user', __name__)
minio_service = MinioService()

@user_controller.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    # Upload the file to MinIO
    result = minio_service.upload_image(file)
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500  
    
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
    user_service = UserService(db=current_app.config['db'])
    profile, message = user_service.get_profile(user_id)
    if not profile:
        return jsonify({"success": False, "error": message }), 404
    return jsonify({"success": True, "profile": profile, "message": message}), 200
