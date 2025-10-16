from rest_framework import serializers
from .models import Cycle, DailyLog, Symptom

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ('id', 'start_date', 'end_date')
        read_only_fields = ('id',)

class DailyLogSerializer(serializers.ModelSerializer):
    symptoms = serializers.PrimaryKeyRelatedField(
        queryset=Symptom.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = DailyLog
        fields = ('date', 'mood', 'pain_level', 'symptoms', 'symptom_severity', 'energy_level', 'notes')
        