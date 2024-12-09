from flask import Blueprint, request, jsonify
from src.services.bucket_service import MinioService

test_minio = Blueprint('test_minio', __name__)
minio_service = MinioService()

@test_minio.route("/upload", methods=["POST"])
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
