import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import quote


IMAGE_DIR = Path(__file__).resolve().parent.parent / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)


def generate_image(prompt):
    try:
        if not prompt:
            prompt = "modern product advertisement"

        # 🔥 encode + add randomness to avoid caching
        safe_prompt = quote(prompt + f" {datetime.now().timestamp()}")

        url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return None, f"Failed: {response.status_code}"

        filename = f"{int(datetime.now().timestamp())}.jpg"
        filepath = IMAGE_DIR / filename

        with open(filepath, "wb") as f:
            f.write(response.content)

        return str(filepath), "success"

    except Exception as e:
        return None, str(e)