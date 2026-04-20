_AESTHETIC_BASE = (
    "analog film photograph, 1973, Kodachrome film grain, "
    "warm earthy tones, faded yellows and burnt oranges, "
    "low contrast, slightly overexposed, vintage lens flare, "
    "35mm documentary photography style, "
    "Vietnam War era American Southwest, "
    "dust and heat haze, weathered surfaces"
)

_DOOR_ANCHOR = (
    "a weathered wooden door at the edge of a dusty road, "
    "golden light beyond the threshold, the door slightly ajar"
)

_NEGATIVE_PROMPT = (
    "digital art, modern, clean, sharp edges, neon, "
    "bright saturated colors, HDR, 3D render, anime, "
    "cartoon, painting, illustration, watermark, signature"
)

_WAR_KEYWORDS = {"war", "soldier", "weapon", "battle", "death", "mortality", "loss", "violence"}
_PEACE_KEYWORDS = {"peace", "transcendence", "release", "freedom", "heaven", "light", "hope"}


def build_image_prompt(analysis: dict) -> tuple[str, str]:
    seeds = analysis.get("image_prompt_seeds", [])
    visual_mood = analysis.get("visual_mood", "")
    themes = [t.lower() for t in analysis.get("themes", [])]

    subject_elements = ", ".join(seeds[:5])

    # Historical grounding — inject period-specific imagery based on themes
    historical_layer = ""
    if any(kw in " ".join(themes) for kw in _WAR_KEYWORDS):
        historical_layer = "Vietnam-era military presence in background, dog tags, letters home, "
    elif any(kw in " ".join(themes) for kw in _PEACE_KEYWORDS):
        historical_layer = "wildflowers in cracked asphalt, birds lifting into open sky, "

    prompt = (
        f"{_AESTHETIC_BASE}, "
        f"{_DOOR_ANCHOR}, "
        f"{subject_elements}, "
        f"{historical_layer}"
        f"{visual_mood}, "
        "cinematic composition, rule of thirds, "
        "solitary human figure in silhouette optional, "
        "profound stillness, liminal space"
    )

    return prompt, _NEGATIVE_PROMPT
