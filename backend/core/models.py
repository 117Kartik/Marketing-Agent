from django.db import models


class Campaign(models.Model):
    # 🔹 INPUTS
    product = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    audience = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_prompt = models.TextField(blank=True, null=True)

    # 🔹 OUTPUT
    headline = models.TextField()
    generated_text = models.TextField()
    hashtags = models.TextField()
    cta = models.TextField()

    # 🔹 IMAGE
    image_path = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.created_at}"