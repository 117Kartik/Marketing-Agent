from apis.llm_api import call_llm
from apis.image_api import generate_image

def creative_agent(data):
    prompt = f"""
    Generate ONLY:

    1. Headline (1 line)
    2. Caption (max 3 lines)
    3. 5 hashtags
    4. Call-to-action (1 line)

    Keep output short and engaging.

    Product: {data['product']}
    Audience: {data['audience']}
    """

    text = call_llm(prompt)
    image_path, image_status = generate_image(data['product'])

    return {
    **data,
    "content": text,
    "image_path": image_path,
    "image_status": image_status
}