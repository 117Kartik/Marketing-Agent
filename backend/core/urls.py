from django.urls import path
from .views import generate_campaign

urlpatterns = [
    path('generate/', generate_campaign),
]