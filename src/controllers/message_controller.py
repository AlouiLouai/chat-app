from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import jwt_required
from src.services.message_service import MessageService
from src.database import db

message_controller = Blueprint('message', __name__)

    
@message_controller.route("/messages", methods=["GET"])
@jwt_required()
def get_messages():
    """
    Endpoint to retrieve the messages of the authenticated user
    """
    try:
        message_service = MessageService(db=db,app=current_app)
        messages = message_service.get_messages()
        return jsonify({"messages": messages}), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_messages: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

    
