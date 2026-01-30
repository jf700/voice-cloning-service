from abc import ABC, abstractmethod
from typing import BinaryIO
from app.schemas.voice import VoiceSettings

class VoiceEngine(ABC):
    """
    Abstract Base Class for Voice Generation Services.
    """

    @abstractmethod
    async def generate_audio(self, text: str, voice_id: str, settings: VoiceSettings) -> BinaryIO:
        """
        Generates audio from text.
        Must return a file-like object (bytes) of the audio.
        """
        pass