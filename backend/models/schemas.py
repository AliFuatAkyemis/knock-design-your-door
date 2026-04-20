from pydantic import BaseModel
from typing import Optional, List


class TranscriptionResult(BaseModel):
    text: str
    language: str
    confidence_note: str


class GeminiAnalysis(BaseModel):
    themes: List[str]
    emotional_tone: str
    dylan_interpretation: str
    connection_to_1973: str
    door_symbolism: str
    visual_mood: str
    image_prompt_seeds: List[str]


class ProcessResponse(BaseModel):
    transcription: TranscriptionResult
    analysis: GeminiAnalysis
    image_prompt: str
    image_url: str
