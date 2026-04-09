from apis.linkedin_api import fetch_user_posts
from apis.llm_api import call_llm

def personalization_agent(data):
    posts = fetch_user_posts()

    prompt = f"""
    Based on user's previous posts:
    {posts}

    Adjust the tone of this:
    {data['content']}
    """

    personalized = call_llm(prompt)

    return {**data, "content": personalized}