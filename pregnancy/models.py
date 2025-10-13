from django.db import models
from users.models import User

class PregnancyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pregnancy_profile')
    estimated_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Pregnancy Profile for {self.user.username}"