from rest_framework import serializers
from .models import PostpartumMoodLog

class PostpartumMoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostpartumMoodLog
        fields = ('date', 'mood')