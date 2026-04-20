"""
Speech-to-text via Groq Whisper API (whisper-large-v3-turbo).
"""
from groq import Groq
from backend.config import settings

_client = Groq(api_key=settings.groq_api_key)


def transcribe(audio_path: str) -> dict:
    with open(audio_path, "rb") as f:
        response = _client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=f,
            response_format="text",
        )
    text = response if isinstance(response, str) else response.text
    return {
        "text": text.strip(),
        "language": "auto-detected",
        "confidence_note": "Groq Whisper Large v3 Turbo",
    }
