"""
POST endpoint for audio transcription.

## Traceability
- Feature: F001, F004 (Voice input support)
"""

import base64

from pydantic import BaseModel

from api.v1.endpoints.transcribe import router
from service.llm.llm_service import LLMService

llm_service = LLMService()


class TranscribeRequest(BaseModel):
    audio_base64: str


class TranscribeResponse(BaseModel):
    text: str


@router.post("", response_model=TranscribeResponse)
async def transcribe_audio(data: TranscribeRequest):
    """Transcribe base64-encoded audio using OpenAI Whisper."""
    audio_bytes = base64.b64decode(data.audio_base64)
    text = await llm_service.transcribe_audio(audio_bytes)
    return TranscribeResponse(text=text)
