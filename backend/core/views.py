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

            if not product or not audience:
                return JsonResponse({"error": "Missing input"}, status=400)

            # 🔥 FULL PIPELINE
            data = ingest(product, audience)

            # merge extra inputs
            data["brand"] = body.get("brand")
            data["description"] = body.get("description")
            data["image_prompt"] = body.get("image_prompt")

            data = creative_agent(data)
            data = personalization_agent(data)
            data = optimizer_agent(data)

            # 🔥 SAVE TO DATABASE
            Campaign.objects.create(
                product=data.get("product"),
                brand=data.get("brand"),
                audience=data.get("audience"),
                description=data.get("description"),

                headline=data["content"].get("headline"),
                caption=data["content"].get("description"),
                hashtags=pyjson.dumps(data["content"].get("hashtags")),
                cta=data["content"].get("cta"),

                image_path=data.get("image_path")
            )

            return JsonResponse({
                "success": True,
                "data": data
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Use POST request"})


# 🔥 HISTORY API
def get_history(request):
    campaigns = Campaign.objects.all().order_by("-created_at")[:20]

    data = []

    for c in campaigns:
        data.append({
            "product": c.product,
            "brand": c.brand,
            "audience": c.audience,
            "headline": c.headline,
            "caption": c.caption,
            "hashtags": json.loads(c.hashtags),
            "cta": c.cta,
            "image_path": c.image_path,
            "created_at": c.created_at
        })

    return JsonResponse({
        "success": True,
        "data": data
    })