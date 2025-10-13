from django.db import models
from users.models import UserProfile

class StaticContent(models.Model):
    class ContentType(models.TextChoices):
        TIP = 'TIP', 'Tip'
        FAQ = 'FAQ', 'Frequently Asked Question'
        GUIDE = 'GUIDE', 'Guide'
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    content_type = models.CharField(max_length=10, choices=ContentType.choices)
    relevant_mode = models.CharField(max_length=20, choices=UserProfile.HealthMode.choices)
    week_of_pregnancy = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Only for pregnancy guides")

    def __str__(self):
        return f"[{self.relevant_mode} {self.content_type}] {self.title}"