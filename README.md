# KNOCK: Design Your Door

> *"Knock, knock, knockin' on heaven's door..."* — Bob Dylan, 1973

A CSE 358 AI Art Project. Upload a cover of Dylan's song; receive a philosophical analysis and a 1973-aesthetic visual artifact.

## How It Works

1. You upload an audio cover of *Knockin' on Heaven's Door*
2. **Whisper** (OpenAI, local — no API key) transcribes the lyrics
3. **Gemini 1.5 Flash** (Google AI) analyzes the transcription for philosophical themes, emotional tone, and connection to 1973's Vietnam War era
4. A 5-layer prompt engineering system builds a Stable Diffusion prompt grounded in 1973 Kodachrome aesthetics
5. **SiliconFlow FLUX.1-schnell** generates the visual artifact

## AI Techniques Used

| Technique | Model | Purpose |
|---|---|---|
| Speech-to-Text | OpenAI Whisper `base` (local) | Lyrics transcription |
| Large Language Model | Google Gemini 1.5 Flash | Philosophical analysis |
| Text-to-Image | SiliconFlow FLUX.1-schnell | 1973-aesthetic image generation |

## Setup

### 1. Get Free API Keys

**Google Gemini:**
1. Go to https://aistudio.google.com
2. Click "Get API key" → "Create API key"
3. Free tier: 1,500 requests/day

**SiliconFlow:**
1. Go to https://siliconflow.cn and sign up
2. Navigate to API Keys section → create a key
3. Free quota available on registration

**Whisper:** No key needed — runs locally.

### 2. System Dependencies

```bash
# Arch/CachyOS
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 3. Install Python Dependencies

```bash
source venv/bin/activate.fish   # or: source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure Environment

Edit `.env` and fill in your API keys:

```
GEMINI_API_KEY=your_key_here
SILICONFLOW_API_KEY=your_key_here
```

### 5. Run

```bash
uvicorn backend.main:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

## Project Structure

```
CSE358_Assignment/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # .env configuration
│   ├── models/schemas.py        # Pydantic models
│   ├── services/
│   │   ├── whisper_service.py   # Local STT
│   │   ├── gemini_service.py    # LLM analysis
│   │   └── siliconflow_service.py  # Image generation
│   └── utils/prompt_engineer.py # 1973 aesthetic prompts
└── frontend/
    ├── index.html
    ├── style.css                # Sepia/film grain UI
    └── app.js
```

## Artistic Statement

Each cover of *Knockin' on Heaven's Door* is an act of interpretation. This system creates a **hermeneutic chain**: Dylan interpreted mortality in 1973 → the cover artist interpreted Dylan → Gemini interprets the cover artist → FLUX interprets Gemini. The system does not generate art; it interprets the interpretation of an interpretation.

The 1973 aesthetic is not nostalgia. It is a diagnostic lens: what does a contemporary performer's relationship to this song reveal about how we still reckon with farewell, mortality, and the threshold between what is and what might lie beyond?

## Dependencies

- FastAPI, Uvicorn, pydantic-settings
- openai-whisper (local)
- google-generativeai
- httpx, Pillow
- ffmpeg (system)
