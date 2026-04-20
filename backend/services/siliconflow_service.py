"""
Image generation via Pollinations.ai (free, no API key required).
"""
import base64
from urllib.parse import quote
import httpx


async def generate_image(prompt: str, negative_prompt: str) -> str:
    encoded = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&model=flux"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    img_b64 = base64.b64encode(response.content).decode()
    return f"data:image/jpeg;base64,{img_b64}"
