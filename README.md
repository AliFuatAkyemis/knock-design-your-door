# KNOCK: Design Your Door

> *"Knock, knock, knockin' on heaven's door..."* — Bob Dylan, 1973

A CSE 358 AI Art Project. Upload a cover of Dylan's song; receive a philosophical analysis and a 1973-aesthetic visual artifact.

## How It Works

1. You upload an audio cover of *Knockin' on Heaven's Door*
2. **Groq Whisper** (`whisper-large-v3-turbo`) transcribes the lyrics via API
3. **Groq Llama 3.3 70B** (`llama-3.3-70b-versatile`) analyzes the transcription for philosophical themes, emotional tone, and connection to 1973's Vietnam War era
4. A 5-layer prompt engineering system builds a Stable Diffusion prompt grounded in 1973 Kodachrome aesthetics
5. **Pollinations.ai Flux** generates the visual artifact (free, no API key required)

## AI Techniques Used

| Technique | Model | Purpose |
|---|---|---|
| Speech-to-Text | Groq Whisper `whisper-large-v3-turbo` | Lyrics transcription |
| Large Language Model | Groq Llama 3.3 70B | Philosophical analysis |
| Text-to-Image | Pollinations.ai Flux | 1973-aesthetic image generation |

## Setup

### 1. Get Free API Key

**Groq (STT + LLM):**
1. Go to https://console.groq.com
2. Navigate to API Keys → Create API key
3. Free tier available on registration

**Pollinations.ai:** No key needed — free and open.

### 2. Install Python Dependencies

```bash
source venv/bin/activate.fish   # or: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` and fill in your API key:

```
GROQ_API_KEY=your_key_here
```

### 4. Run

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
│   │   ├── whisper_service.py   # Groq Whisper STT
│   │   ├── gemini_service.py    # Groq LLM analysis
│   │   └── siliconflow_service.py  # Pollinations.ai image generation
│   └── utils/prompt_engineer.py # 1973 aesthetic prompts
└── frontend/
    ├── index.html
    ├── style.css                # Sepia/film grain UI
    └── app.js
```

## Artistic Statement

Each cover of *Knockin' on Heaven's Door* is an act of interpretation. This system creates a **hermeneutic chain**: Dylan interpreted mortality in 1973 → the cover artist interpreted Dylan → Llama interprets the cover artist → Flux interprets Llama. The system does not generate art; it interprets the interpretation of an interpretation.

The 1973 aesthetic is not nostalgia. It is a diagnostic lens: what does a contemporary performer's relationship to this song reveal about how we still reckon with farewell, mortality, and the threshold between what is and what might lie beyond?

## Dependencies

- FastAPI, Uvicorn, pydantic-settings
- groq
- httpx, Pillow
