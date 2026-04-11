from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt):
    if len(prompt) > 1000:
        return "Prompt too long. Please shorten input."
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}],
                max_tokens=300
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"