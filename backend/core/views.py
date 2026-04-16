import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BASE_DIR)

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from agents.publishing_agent import send_emails
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from agents.publishing_agent import send_emails


from agents.ingestion_agent import ingest
from agents.creative_agent import creative_agent
from agents.personalization_agent import personalization_agent
from agents.optimizer_agent import optimizer_agent
from agents.publishing_agent import send_emails

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

            # PIPELINE
            data = ingest(product, audience)

            data["brand"] = brand
            data["description"] = description
            data["image_prompt"] = image_prompt

            data = creative_agent(data)

            # SAFETY CHECK
            if "content" not in data:
                return JsonResponse({
                    "success": False,
                    "error": "AI failed to generate content"
                })

            # OPTIONAL AGENTS (SAFE)
            try:
                data = personalization_agent(data)
                data = optimizer_agent(data)
            except Exception as e:
                print("Optional agent error:", str(e))

            # SAVE SAFELY
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

    # ONLY ONE RETURN HERE
    return JsonResponse({"message": "Use POST request"})

from django.http import JsonResponse
import json
from core.models import Campaign

def get_history(request):
    campaigns = Campaign.objects.all().order_by("-created_at")[:10]

    data = []

    for c in campaigns:
        data.append({
            "id": c.id,   

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

@csrf_exempt
def publish_campaign(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")

            if not file:
                return JsonResponse({"error": "No file uploaded"}, status=400)

            # GET
            campaign_id = request.POST.get("campaign_id")


            # 🔹 Save file temporarily
            file_path = f"temp_{file.name}"
            with open(file_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # 🔹 UPDATED: SELECT CAMPAIGN
            if campaign_id:
                latest = Campaign.objects.filter(id=campaign_id).first()
            else:
                latest = Campaign.objects.last()

            # STEP 2: CHECK IF EXISTS
            if not latest:
                return JsonResponse({
                    "success": False,
                    "error": "No campaign found. Generate one first."
                }, status=400)

            # STEP 3: SAFE HASHTAGS
            try:
                hashtags = json.loads(latest.hashtags) if latest.hashtags else []
            except:
                hashtags = []

            image_url = f"http://127.0.0.1:8000{latest.image_path}" if latest.image_path else ""

            # STEP 4: BUILD CAMPAIGN DATA
            image_url = f"http://127.0.0.1:8000{latest.image_path}" if latest.image_path else ""

            campaign_data = {
                "brand": latest.brand or "YourBrand",   # 🔥 keep brand at top level

                "content": {
                    "headline": latest.headline or "",
                    "description": latest.generated_text or "",
                    "hashtags": hashtags,
                    "cta": latest.cta or ""
                },

                "image_url": image_url
            }

            # 🔹 UPDATED: PASS EMAIL CREDENTIALS
            success, msg = send_emails(file_path, campaign_data)

            return JsonResponse({
                "success": success,
                "message": msg
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "POST only"})