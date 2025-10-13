from django.db import models
from users.models import User

class PostpartumMoodLog(models.Model):
    class Mood(models.TextChoices):
        HAPPY = 'HAPPY', 'Happy'
        ANXIOUS = 'ANXIOUS', 'Anxious'
        OVERWHELMED = 'OVERWHELMED', 'Overwhelmed'
        TIRED = 'TIRED', 'Tired'
        JOYFUL = 'JOYFUL', 'Joyful'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postpartum_logs')
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=Mood.choices)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Postpartum log for {self.user.username} on {self.date}"