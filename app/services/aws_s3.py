import boto3
import uuid
from botocore.exceptions import NoCredentialsError
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file(self, file_obj, object_name: str = None, content_type: str = "audio/mpeg") -> str:
        """
        Uploads a file-like object to S3 and returns the public URL.
        """
        if object_name is None:
            # Generate a unique filename using UUID
            object_name = f"{uuid.uuid4()}.mp3"

        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Construct the public URL (assuming bucket is public or using presigned URLs)
            # For this demo, we assume a standard S3 virtual-hosted-style URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{object_name}"
            return url, object_name

        except NoCredentialsError:
            print("Credentials not available")
            return None, None
        except Exception as e:
            print(f"Failed to upload to S3: {e}")
            raise e