import os
import shutil
import tempfile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.models.schemas import GeminiAnalysis, ProcessResponse, TranscriptionResult
from backend.services import gemini_service, siliconflow_service, whisper_service
from backend.utils.prompt_engineer import build_image_prompt

os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.output_dir, exist_ok=True)

app = FastAPI(title="Knock: Design Your Door", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "alive", "stt": "groq-whisper", "analysis": "groq-llama3", "image": "pollinations"}


@app.post("/api/process", response_model=ProcessResponse)
async def process_cover(
    audio: UploadFile = File(...),
    cover_artist: str = Form(default="Unknown Artist"),
    cover_year: str = Form(default=""),
    cover_style: str = Form(default="acoustic"),
):
    # Validate file size
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    audio_bytes = await audio.read()
    if len(audio_bytes) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_upload_size_mb}MB.",
        )

    suffix = os.path.splitext(audio.filename or "cover.mp3")[1] or ".mp3"
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, dir=settings.upload_dir
    ) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        # Step 1: Transcribe with Whisper (local)
        transcription_data = whisper_service.transcribe(tmp_path)

        # Step 2: Philosophical analysis with Gemini
        metadata = {
            "cover_artist": cover_artist,
            "cover_year": cover_year or "Unknown",
            "cover_style": cover_style,
        }
        analysis_data = gemini_service.analyze(transcription_data["text"], metadata)

        # Step 3: Build 1973-aesthetic image prompt
        image_prompt, negative_prompt = build_image_prompt(analysis_data)

        # Step 4: Generate image via SiliconFlow
        image_url = await siliconflow_service.generate_image(image_prompt, negative_prompt)

        return ProcessResponse(
            transcription=TranscriptionResult(**transcription_data),
            analysis=GeminiAnalysis(**analysis_data),
            image_prompt=image_prompt,
            image_url=image_url,
        )
    finally:
        os.unlink(tmp_path)


# Serve frontend last so API routes take priority
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
