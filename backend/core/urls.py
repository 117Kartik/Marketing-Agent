from django.urls import path
from .views import generate_campaign, get_history, publish_campaign

urlpatterns = [
    path('generate/', generate_campaign),
    path('history/', get_history),
    path('history/', get_history),
    path('publish/', publish_campaign),
]