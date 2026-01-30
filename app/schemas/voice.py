from pydantic import BaseModel, Field, HttpUrl
from typing import Optional



class VoiceSettings(BaseModel):
    """
    Fine-tunes the emotion and delivery of the voice.
    Mapped to ElevenLabs/Cartesia parameters.
    """

    stability: float = Field(
        0.5, 
        ge=0.0, le=1.0, 
        description="Lower = more emotion/randomness. Higher = more stable/monotone."
    )
    similarity_boost: float = Field(
        0.75, 
        ge=0.0, le=1.0, 
        description="How closely the AI mimics the original voice."
    )
    speed: float = Field(
        1.0, 
        ge=0.5, le=2.0, 
        description="Playback speed multiplier (1.0 is normal)."
    )

class TTSRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=5000, 
        description="The text content to convert to speech."
    )
    voice_id: str = Field(
        ..., 
        description="The unique ID of the voice model."
    )
    settings: Optional[VoiceSettings] = Field(
        default_factory=VoiceSettings,
        description="Optional overrides for voice stability and emotion."
    )

class TTSResponse(BaseModel):
    """
    Returns the location of the generated audio file.
    """
    file_name: str
    s3_url: HttpUrl  # Pydantic validates this is a real URL structure
    duration_seconds: Optional[float] = None
    status: str = "completed"