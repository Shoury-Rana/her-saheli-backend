from django.db import models
from users.models import User

class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycles')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"Cycle for {self.user.username} starting {self.start_date}"

class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class DailyLog(models.Model):
    class Mood(models.TextChoices):
        HAPPY = 'HAPPY', 'Happy'
        SAD = 'SAD', 'Sad'
        ANXIOUS = 'ANXIOUS', 'Anxious'
        IRRITABLE = 'IRRITABLE', 'Irritable'
        ENERGETIC = 'ENERGETIC', 'Energetic'
        FATIGUED = 'FATIGUED', 'Fatigued'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=Mood.choices, null=True, blank=True)
    pain_level = models.PositiveSmallIntegerField(null=True, blank=True) # e.g., 0-5
    symptoms = models.ManyToManyField(Symptom, blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Log for {self.user.username} on {self.date}"