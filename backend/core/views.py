from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Add root path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from agents.ingestion_agent import ingest
from agents.creative_agent import creative_agent
from agents.personalization_agent import personalization_agent
from agents.optimizer_agent import optimizer_agent

from core.models import Campaign   # ✅ IMPORTANT
import json as pyjson


def home(request):
    return HttpResponse("AI Marketing Agent is running!")


@csrf_exempt
def generate_campaign(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            product = body.get("product")
            audience = body.get("audience")
            brand = body.get("brand")
            description = body.get("description")
            image_prompt = body.get("image_prompt")

            if not product or not audience:
                return JsonResponse({"error": "Missing input"}, status=400)

            # 🔹 PIPELINE
            data = ingest(product, audience)

            data["brand"] = brand
            data["description"] = description
            data["image_prompt"] = image_prompt

            data = creative_agent(data)

            # 🔥 SAFETY CHECK
            if "content" not in data:
                return JsonResponse({
                    "success": False,
                    "error": "AI failed to generate content"
                })

            # 🔥 OPTIONAL AGENTS (SAFE)
            try:
                data = personalization_agent(data)
                data = optimizer_agent(data)
            except Exception as e:
                print("Optional agent error:", str(e))

            # 🔥 SAVE SAFELY
            try:
                Campaign.objects.create(
                    product=product,
                    brand=brand,
                    audience=audience,
                    description=description,
                    image_prompt=image_prompt,

                    headline=data["content"].get("headline", ""),
                    generated_text=data["content"].get("description", ""),
                    hashtags=json.dumps(data["content"].get("hashtags", [])),
                    cta=data["content"].get("cta", ""),

                    image_path=data.get("image_path")
                )
            except Exception as e:
                print("DB SAVE ERROR:", str(e))

            return JsonResponse({
                "success": True,
                "data": data
            })

        except Exception as e:
            print("MAIN ERROR:", str(e))
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    # ✅ ONLY ONE RETURN HERE
    return JsonResponse({"message": "Use POST request"})

def get_history(request):
    campaigns = Campaign.objects.all().order_by("-created_at")[:10]

    data = []

    for c in campaigns:
        data.append({
            "product": c.product,
            "brand": c.brand,
            "audience": c.audience,
            "description": c.description,
            "image_prompt": c.image_prompt,

            "content": {
                "headline": c.headline,
                "description": c.generated_text,
                "hashtags": json.loads(c.hashtags) if c.hashtags else [],
                "cta": c.cta
            },

            "image_path": c.image_path
        })

    return JsonResponse({
        "success": True,
        "data": data
    })