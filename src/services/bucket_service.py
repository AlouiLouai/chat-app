from datetime import timedelta
from minio import Minio
from minio.error import S3Error
import os
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename

class BucketService:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ROOT_USER"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
            secure=False  # Disable SSL for local development
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")
        
        # Ensure the bucket exists
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise Exception(f"Error checking or creating bucket: {str(e)}")

    def upload_image(self, file):
        try:
            # Secure the filename
            filename = secure_filename(file.filename)

            # Open the image using Pillow
            img = Image.open(file)
            
            # Resize the image if necessary (example: max 1024x1024)
            max_size = (1024, 1024)
            img.thumbnail(max_size)

            # Save the resized image to a BytesIO object
            img_byte_array = BytesIO()
            img_format = img.format if img.format else "PNG"  # Default to PNG if format is unknown
            img.save(img_byte_array, format=img_format)
            img_byte_array.seek(0)

            # Upload the resized image to MinIO
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=img_byte_array,
                length=img_byte_array.getbuffer().nbytes,
                content_type=f'image/{img_format.lower()}',
            )

            # Generate the pre-signed URL for private access to the uploaded image
            expires_duration = timedelta(seconds=3600)
            presigned_url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                expires=expires_duration,  # URL valid for 1 hour
            )

            # Generate the URL for the uploaded image
            public_url = f"http://{os.getenv('MINIO_ENDPOINT')}/{self.bucket_name}/{filename}"
            
            return {
                "success": True,
                "url": public_url,
                "presigned_url": presigned_url,
            }

        except S3Error as e:
            return {"success": False, "error": f"S3 Error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected Error: {str(e)}"}
