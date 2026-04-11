from apis.llm_api import call_llm
import json


def optimizer_agent(data):
    content = data["content"]

    prompt = f"""
You are a marketing optimizer.

Improve clarity, engagement, and make it more catchy.

Return STRICT JSON only:

{{
  "headline": "...",
  "caption": "...",
  "hashtags": ["...", "...", "...", "...", "..."],
  "cta": "..."
}}

Content:
{content}
"""

    text = call_llm(prompt)

    try:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid response")

        clean_text = text.strip()

        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]

        parsed = json.loads(clean_text)

        data["content"].update(parsed)

    except Exception:
        pass

    return data