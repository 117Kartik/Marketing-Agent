from django.db import models

class Campaign(models.Model):
    product = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    audience = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    headline = models.TextField()
    caption = models.TextField(blank=True, null=True)
    hashtags = models.TextField()
    cta = models.TextField()

    image_path = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product