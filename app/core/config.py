from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cloud-Native Voice Service"
    API_V1_STR: str = "/api/v1"
    
    # AWS Settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str

    # Voice Provider Keys
    ELEVENLABS_API_KEY: str
    # CARTESIA_API_KEY: str  # Add this when you are ready

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()