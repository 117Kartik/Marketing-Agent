from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Add root project path so Django can access your agents
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from agents.ingestion_agent import ingest
from agents.creative_agent import creative_agent
from agents.personalization_agent import personalization_agent
from agents.optimizer_agent import optimizer_agent
from django.http import HttpResponse

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

            # Run your pipeline
            data = ingest(product, audience)
            data = creative_agent(data)
            data = personalization_agent(data)
            data = optimizer_agent(data)

            return JsonResponse({
                "success": True,
                "data": data
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Use POST request"})