from apis.llm_api import call_llm
from apis.image_api import generate_image
import json


def creative_agent(data):
    prompt = f"""
You are a marketing AI.

Return output STRICTLY in this JSON format:

{{
  "headline": "...",
  "caption": "...",
  "hashtags": ["...", "...", "...", "...", "..."],
  "cta": "..."
}}

Rules:
- No extra text
- No explanation
- Only JSON
- Keep caption short (2–3 lines max)

Product: {data['product']}
Audience: {data['audience']}
"""

    text = call_llm(prompt)
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid response")

        clean_text = text.strip()

        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]

        parsed = json.loads(clean_text)

    except Exception:
        parsed = {
            "headline": "Parsing Error",
            "caption": str(text),
            "hashtags": [],
            "cta": ""
        }

    # Image generation
    image_path, image_status = generate_image(data['product'])

    return {
        **data,
        "content": parsed,
        "raw_output": text,
        "image_path": image_path,
        "image_status": image_status
    }