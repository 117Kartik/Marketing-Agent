from apis.llm_api import call_llm
from apis.image_api import generate_image


def creative_agent(data):
    prompt = f"""
    Create a marketing campaign:

    Product: {data['product']}
    Audience: {data['audience']}

    Give:
    - Headline
    - Caption
    - Hashtags
    """

    text = call_llm(prompt)
    image = generate_image(data['product'])

    return {**data, "content": text, "image": image}