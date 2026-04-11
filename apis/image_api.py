import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import base64
import uuid

# Load env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("STABILITY_API_KEY")

# Folder to store images
IMAGE_DIR = Path(__file__).resolve().parent.parent / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)

def generate_image(prompt):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    data = {
        "prompt": f"Professional marketing poster of {prompt}, modern, high quality",
        "output_format": "png"
    }

    response = requests.post(url, headers=headers, files={"none": ''}, data=data)

    if response.status_code != 200:
        return None, f"Image generation failed: {response.text}"

    image_data = response.json()

    # 🔥 Extract base64 image
    image_base64 = image_data["image"]

    # 🔥 Generate unique filename
    filename = f"{uuid.uuid4()}.png"
    filepath = IMAGE_DIR / filename

    # 🔥 Save image
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_base64))

    return str(filepath), "Image saved successfully"