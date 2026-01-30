from fastapi import APIRouter
from app.api.v1.endpoints import voice

api_router = APIRouter()

# Include the voice routes under the "/voice" prefix
# resulting URL: /api/v1/voice/generate
api_router.include_router(voice.router, prefix="/voice", tags=["Voice Generation"])