from apis.llm_api import call_llm
from apis.image_api import generate_image
import os
import random


def creative_agent(data):
    prompt = f"""
You are a professional marketing strategist.

Create HIGH-QUALITY marketing content.

STRICT RULES:
- MUST use product, brand, description
- Avoid generic phrases

FORMAT:

HEADLINE:
...

DESCRIPTION:
...

HASHTAGS:
#tag1 #tag2 #tag3 (max 3 tags)

CTA:
...

INPUT:
Product: {data.get('product')}
Brand: {data.get('brand')}
Audience: {data.get('audience')}
Description: {data.get('description')}
"""

    # 🔥 CALL LLM
    text = call_llm(prompt)

    # ✅ ensure safe string
    if not text or not isinstance(text, str):
        text = ""

    parsed = {
        "headline": "",
        "description": "",
        "hashtags": [],
        "cta": ""
    }

    try:
        clean_text = text.strip()
        sections = clean_text.split("\n\n")

        for section in sections:
            if section.startswith("HEADLINE:"):
                parsed["headline"] = section.replace("HEADLINE:", "").strip()

            elif section.startswith("DESCRIPTION:"):
                parsed["description"] = section.replace("DESCRIPTION:", "").strip()

            elif section.startswith("HASHTAGS:"):
                raw_tags = section.replace("HASHTAGS:", "").strip().split()
                raw_tags = [t.strip() for t in raw_tags if t.strip()]
                parsed["hashtags"] = raw_tags

            elif section.startswith("CTA:"):
                parsed["cta"] = section.replace("CTA:", "").strip()

    except Exception:
        parsed["description"] = text

    # 🚀 -------- CONTROL AI OUTPUT --------

    # 🔥 FIX + LIMIT HASHTAGS
    if isinstance(parsed["hashtags"], list):
        fixed_tags = []

        for tag in parsed["hashtags"][:3]:
            tag = tag.strip()

            if not tag.startswith("#"):
                tag = f"#{tag}"

            tag = tag.replace(",", "").replace(".", "")

            fixed_tags.append(tag)

        parsed["hashtags"] = fixed_tags
    else:
        parsed["hashtags"] = []

    # 🔥 ENFORCE DESCRIPTION WORD LIMIT (100–200 words)
    if parsed["description"]:
        words = parsed["description"].split()

        # If too short → repeat intelligently
        if len(words) < 100:
            repeat_text = parsed["description"]
            while len(words) < 100:
                words += repeat_text.split()

        # Trim to max 200 words
        words = words[:200]

        parsed["description"] = " ".join(words)

    else:
        parsed["description"] = "High-quality product designed for modern users. Reliable, efficient, and built to deliver consistent performance in everyday use."

    # 🚀 -------- IMAGE GENERATION --------

    image_prompt = f"""
{data.get('brand') or ''} {data.get('product')},
for {data.get('audience')},
{data.get('description') or ''},

clean product advertisement,
modern marketing poster,
studio lighting,
high quality,
realistic,
centered product,
minimal background,

brand logo placement at top left,
clean typography,
professional layout,
advertisement style composition
"""

    # 🔥 RANDOMNESS
    image_prompt += f", variation {random.randint(1, 10000)}"

    print("IMAGE PROMPT:", image_prompt)

    image_path, image_status = generate_image(image_prompt)

    print("IMAGE STATUS:", image_status)

    # 🔥 FALLBACK IF IMAGE FAILS
    if not image_path:
        image_prompt += ", simple clean product shot"
        image_path, image_status = generate_image(image_prompt)

    # 🔥 MEDIA PATH FIX
    if image_path and isinstance(image_path, str):
        filename = os.path.basename(image_path)
        media_path = f"/media/{filename}"
    else:
        media_path = None

    return {
        **data,
        "content": parsed,
        "raw_output": text,
        "image_path": media_path,
        "image_status": image_status
    }