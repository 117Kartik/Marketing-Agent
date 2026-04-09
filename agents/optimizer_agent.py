from apis.llm_api import call_llm

def optimizer_agent(data):
    prompt = f"""
    Improve this content for engagement:

    {data['content']}

    Add strong CTA and hooks.
    """

    optimized = call_llm(prompt)

    return {**data, "content": optimized}