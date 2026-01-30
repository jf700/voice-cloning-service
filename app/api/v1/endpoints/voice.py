from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.voice import TTSRequest, TTSResponse
from app.services.elevenlabs_service import ElevenLabsService
from app.services.aws_s3 import S3Service

router = APIRouter()

# Dependency Injection Helpers
def get_voice_service():
    return ElevenLabsService()

def get_storage_service():
    return S3Service()

@router.post("/generate", response_model=TTSResponse, status_code=status.HTTP_201_CREATED)
async def generate_speech(
    request: TTSRequest,
    voice_service: ElevenLabsService = Depends(get_voice_service),
    storage_service: S3Service = Depends(get_storage_service)
):
    """
    1. Receives text and emotion settings.
    2. Asynchronously calls ElevenLabs (Concurrent I/O).
    3. Uploads the resulting audio stream directly to S3.
    4. Returns a secure URL for playback.
    """
    try:
        # 1. Generate Audio (Async - doesn't block other requests)
        # We pass the settings from the request to control emotion/stability
        audio_stream = await voice_service.generate_audio(
            text=request.text,
            voice_id=request.voice_id,
            voice_settings=request.settings
        )
        
        # 2. Upload to S3
        # We create a filename based on the voice ID for tracking
        s3_url, object_name = storage_service.upload_file(
            audio_stream, 
            content_type="audio/mpeg"
        )
        
        if not s3_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Failed to upload audio to storage."
            )

        # 3. Return Response
        return TTSResponse(
            file_name=object_name,
            s3_url=s3_url,
            status="completed"
        )

    except Exception as e:
        # In a real app, log the error here (e.g., sentry or cloudwatch)
        raise HTTPException(status_code=500, detail=str(e))