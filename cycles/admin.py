from django.contrib import admin
from .models import Cycle, Symptom, DailyLog

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date')
    search_fields = ('user__username',)
    list_filter = ('start_date',)

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood', 'pain_level')
    search_fields = ('user__username',)
    list_filter = ('date', 'mood')
    filter_horizontal = ('symptoms',)