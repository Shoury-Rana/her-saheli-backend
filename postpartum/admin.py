from django.contrib import admin
from .models import PostpartumMoodLog

@admin.register(PostpartumMoodLog)
class PostpartumMoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood')
    search_fields = ('user__username',)
    list_filter = ('mood', 'date')