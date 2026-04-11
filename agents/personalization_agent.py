from apis.llm_api import call_llm
import json


def personalization_agent(data):
    content = data["content"]

    prompt = f"""
You are a marketing expert.

Improve tone and make it more appealing for the target audience.

Return STRICT JSON only:

{{
  "headline": "...",
  "caption": "...",
  "hashtags": ["...", "...", "...", "...", "..."],
  "cta": "..."
}}

Audience: {data['audience']}

Content:
Headline: {content.get("headline")}
Caption: {content.get("caption")}
CTA: {content.get("cta")}
"""

    text = call_llm(prompt)

    try:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid response")

        clean_text = text.strip()

        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]

        parsed = json.loads(clean_text)

        # Merge updates
        data["content"].update(parsed)

    except Exception:
        pass  # keep original if fails

    return data