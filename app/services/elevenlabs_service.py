import httpx
import io
from app.services.voice_engine import VoiceEngine
from app.schemas.voice import VoiceSettings
from app.core.config import settings

class ElevenLabsService(VoiceEngine):
    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    async def generate_audio(self, text: str, voice_id: str, voice_settings: VoiceSettings) -> io.BytesIO:
        """
        Calls ElevenLabs API to convert text to speech.
        """
        url = f"{self.BASE_URL}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": voice_settings.stability,
                "similarity_boost": voice_settings.similarity_boost,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers, timeout=30.0)
            
            if response.status_code != 200:
                raise Exception(f"ElevenLabs API Error: {response.text}")

            # Return binary content as a file-like object
            return io.BytesIO(response.content)

    async def get_voices(self):
        """
        Optional: Helper to list available voices
        """
        url = f"{self.BASE_URL}/voices"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            return response.json()