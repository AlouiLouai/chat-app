from minio import Minio
from minio.error import S3Error
import os
from werkzeug.utils import secure_filename

class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
            secure=False  # Disable SSL for local development
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME",)
        
        # Ensure the bucket exists
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_image(self, file):
        try:
            # Secure the filename
            filename = secure_filename(file.filename)

            # Upload the file to MinIO
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=file.stream,
                length=file.content_length,
                content_type=file.mimetype,
            )

            # Generate the URL for the uploaded image
            image_url = f"http://{os.getenv('MINIO_ENDPOINT')}/{self.bucket_name}/{filename}"
            return {"success": True, "url": image_url}
        except S3Error as e:
            return {"success": False, "error": str(e)}

