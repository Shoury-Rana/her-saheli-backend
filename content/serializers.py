from rest_framework import serializers
from .models import StaticContent

class StaticContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticContent
        fields = ('id', 'title', 'body', 'content_type', 'relevant_mode', 'week_of_pregnancy')