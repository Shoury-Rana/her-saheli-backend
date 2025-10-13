from rest_framework import serializers
from .models import PregnancyProfile

class PregnancyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PregnancyProfile
        fields = ('estimated_due_date',)