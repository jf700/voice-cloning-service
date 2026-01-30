from pydantic import BaseModel, HttpUrl
from datetime import datetime

class FileUploadResponse(BaseModel):
    """
    Standard response after uploading a file to S3.
    """
    filename: str
    content_type: str
    size_bytes: int
    s3_url: HttpUrl
    uploaded_at: datetime = datetime.now()