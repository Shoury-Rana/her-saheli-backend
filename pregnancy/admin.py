from django.contrib import admin
from .models import PregnancyProfile

@admin.register(PregnancyProfile)
class PregnancyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'estimated_due_date')
    search_fields = ('user__username',)