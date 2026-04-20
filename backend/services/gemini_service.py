import json
from groq import Groq
from backend.config import settings

_client = Groq(api_key=settings.groq_api_key)

_PROMPT_TEMPLATE = """
You are an art critic and cultural historian specializing in 1973 American counterculture.

A performer has recorded a cover of Bob Dylan's "Knockin' on Heaven's Door" (1973).
This song was written for the film "Pat Garrett & Billy the Kid" during the Vietnam War era.
It explores themes of: mortality, farewell, laying down weapons, peace before death,
and the boundary between earthly life and what lies beyond.

== COVER METADATA ==
Artist: {cover_artist}
Year Recorded: {cover_year}
Style: {cover_style}

== TRANSCRIBED LYRICS FROM THIS COVER ==
{transcription}

== YOUR TASK ==
Analyze this specific cover version and respond in valid JSON with these exact keys:
- "themes": list of 3-5 philosophical themes present in HOW this performer sang it
- "emotional_tone": one paragraph on the emotional character of this performance
- "dylan_interpretation": how does this cover reinterpret Dylan's original intent?
- "connection_to_1973": how does this performance connect to Vietnam War era, mortality, and counterculture?
- "door_symbolism": what does "the door" represent specifically in this version's emotional register?
- "visual_mood": describe the visual atmosphere this performance evokes (for image generation), in 2-3 sentences
- "image_prompt_seeds": list of 5-7 concrete visual elements for an image prompt (nouns and adjectives only)

Respond ONLY with the JSON object. No markdown fences, no explanation, no preamble.
""".strip()


def analyze(transcription: str, metadata: dict) -> dict:
    prompt = _PROMPT_TEMPLATE.format(
        cover_artist=metadata.get("cover_artist", "Unknown"),
        cover_year=metadata.get("cover_year", "Unknown"),
        cover_style=metadata.get("cover_style", "Unknown"),
        transcription=transcription,
    )

    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "themes": ["mortality", "farewell", "transcendence"],
            "emotional_tone": "The cover carries a profound sense of quiet resignation and acceptance.",
            "dylan_interpretation": "This performance stays close to Dylan's mournful original intention.",
            "connection_to_1973": "Like the Vietnam era, this performance acknowledges the cost of violence and longs for peace.",
            "door_symbolism": "The door represents the threshold between suffering and release.",
            "visual_mood": "Dusty, golden, and still. Late afternoon light over an empty road.",
            "image_prompt_seeds": ["weathered wood", "golden dust", "empty road", "lone figure", "fading light"],
        }
